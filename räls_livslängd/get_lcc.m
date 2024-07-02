function [lcc_total, rail_lifetime] = get_lcc(H_table, NW_table, maint_strategy, type, gauge_widening, max_lifetime, renewal_costs)
%GET_LCC calculates the total lifecycle costs
%   Given a maintenance strategy (frequency of tamping/grinding), the
%   function estimates the total LCC in net present value

discount_rate = 0.04; % 4%

% Track parameters
track_length_meter = 1000; 
track_lifetime_years = 15;

% Cost parameters (sek/m)
tamping_cost_per_meter = 40;
grinding_cost_per_meter = 50;

% maintenance frequency
grinding_freq = maint_strategy(1);
tamping_freq = maint_strategy(2);

% train operation parameters (SEk per hour)
cost_hourly_poss = 50293;

% track possession per activity (in hours)
poss_grinding = 2;
poss_tamping = 2;
%poss_grinding_MB6 = 3;

% gauge intervals (in mm)
gauge = [1440,1445,1450,1455];
% if(strcmp(inner_rail,"MB6"))
%     gauge = gauge(3:4);
% end

Xq = gauge;

% get max months before grinding
max_months_grinding = size(H_table, 2);

% months (for interpolation)
months = 1:max_months_grinding;
Yq= months;

% maximum H (criterion for rail renewal)
H_max = 14;

% find the corresponding total LCC 
H_curr = 0;
gauge_curr = gauge(1);
maintenance = 0;
train_op = 0;
latest_grinding_since = 1; % in months
latest_tamping_since = 1; % in months
rail_lifetime = 15;
max_m = 12*track_lifetime_years;
lifetime_remainder = max_m;


%%% renewal cost
% Renewal cost (Material + Work) in SEK per meter
% if(strcmp(inner_rail,"MB6"))
%     renewal_costs =2214;  %500+924.7;% 
% end
% renewal_costs = 1500;%500+924.4;%; 
% total renewl cost
renewal = renewal_costs*track_length_meter;

gauge_curr_historic = zeros(1, max_m);
H_curr_historic = zeros(1, max_m);

%%% simulation of LCC
for m=1:max_m % till track lifetime
    
    %%% convert month to year
    y = m/12; % ceil(m/12);
    
    %%% gauge increase after 1 month
    avg_yearly_gauge_widening = interp1(Xq, gauge_widening(:),gauge_curr,type);
    gauge_curr = gauge_curr+avg_yearly_gauge_widening/12;
    gauge_curr_historic(m) = gauge_curr;
    
    lifetime_remainder = lifetime_remainder-1;
    % calculate the marginal increase delta_H
    delta_H = interp2(Yq,Xq, NW_table(:,Yq),latest_grinding_since,gauge_curr,type);
        
    % Grinding and its costs
    if(latest_grinding_since==grinding_freq) % time to do grinding
        maintenance = maintenance + grinding_cost_per_meter*track_length_meter/(1+discount_rate)^y; 
        latest_grinding_since = 0;
        train_op = train_op + poss_grinding*cost_hourly_poss/(1+discount_rate)^y;
        % update the H-index using + H_index - natural wear
        H_curr = H_curr + interp2(Yq,Xq, H_table(:,Yq),grinding_freq,gauge_curr,type) - delta_H;
        if(isnan(H_curr))
            H_curr
        end
    else
        %%% update the current H-index
        % update
        H_curr = H_curr + delta_H;
        if(isnan(H_curr))
            H_curr;
        end
    end
    H_curr_historic(m) = H_curr;
    
    % Tamping and its costs
    if(latest_tamping_since==tamping_freq) % time to do tamping
        maintenance = maintenance + tamping_cost_per_meter*track_length_meter/(1+discount_rate)^y;
        train_op = train_op + poss_tamping*cost_hourly_poss/(1+discount_rate)^y;
        gauge_curr = gauge(1);
        latest_tamping_since = 0;
        lifetime_remainder = max_m;
    end
    
    % stop if we need to renew the rail or if we are beyond the maximal gauge limit
    % include remaining_lifetime using max_lifetime (from risk tables)
    if(H_curr>H_max || lifetime_remainder == 0)
        rail_lifetime = y; % return lifetime in years
        break;
    end
    
    %%% too high gauge, i.e., risk for derailment 
    if(gauge_curr>=1450)
        if(lifetime_remainder > max_lifetime(3))
            lifetime_remainder = max_lifetime(3);
        end
    end
            
    % older grindng and tamping
    latest_grinding_since = latest_grinding_since + 1; % in months
    latest_tamping_since = latest_tamping_since + 1; % in months
    
end

% after end of track life, get the remaining residual from last renewal
% end_of_life = 0;%-get_renewal_cost(track_lifetime_years, inner_rail)*(rail_lifetime-mod(track_lifetime_years,rail_lifetime))/rail_lifetime;

% total LCC in NPV/meter
lcc_total = train_op +maintenance+renewal;%+end_of_life;
lcc_total = lcc_total/track_length_meter/rail_lifetime;


%%% print historical values of H_index and Gauge
% figure;
% yyaxis left;
% plot(H_curr_historic, '-b', 'LineWidth', 2);
% ylabel('H');
% xlabel('Age in Months');
% grid on;
% yyaxis right;
% plot(gauge_curr_historic, '-r', 'LineWidth', 2);
% ylabel('Gauge');
% ylim([1440, 1455])
% title('H and Gauge vs Time');
% legend({'H', 'Gauge'}, 'Location', 'best');


end