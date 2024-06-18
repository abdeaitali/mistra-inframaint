function [lcc_total, rail_lifetime] = get_lcc(H_table, maint_strategy, type, inner_rail, avg_yearly_gauge_widening, max_lifetime)
%GET_LCC calculates the total lifecycle costs
%   Given a maintenance strategy (frequency of tamping/grinding), the
%   function estimates the total LCC in net present value

discount_rate = 0.035; % 4%

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

% months
months = 1:12;
Yq= months;

% maximum H (criterion for rail renewal)
H_max = 14;

% find the corresponding total LCC 
H_curr = 0;
gauge_curr = gauge(1);
renewal = get_renewal_cost(0, inner_rail); % initial renewal
maintenance = 0;
train_op = 0;
latest_grinding_since = 1; % in months
latest_tamping_since = 1; % in months
rail_lifetime = 15;
lifetime_remainder = max_lifetime(1);%12;
max_m = 12*track_lifetime_years;


% average monthly delta_H until next grinding
gauge_grinding = gauge(1) + avg_yearly_gauge_widening/12*(1+mod(grinding_freq-1, tamping_freq));

for m=1:max_m % till track lifetime
    
    % convert month to year
    y = m/12; % ceil(m/12);
    
    % gauge increase after 1 month
    gauge_curr = gauge_curr+avg_yearly_gauge_widening/12;
    

%     lifetime_remainder = lifetime_remainder-1;
    
    % update the X-index
    if(grinding_freq<=12)
        delta_H = interp2(Yq,Xq, H_table(:,Yq),grinding_freq,gauge_grinding,type);
    else
        ext_H_table = H_table(1,Yq);
        for i=1:12
            ext_H_table(1,i) = interp2(Yq,Xq, H_table(:,Yq),i,gauge_grinding,type);
        end
        delta_H = interp1(1:12, ext_H_table(1,:), grinding_freq, type, 'extrap');      
    end
    delta_H_monthly = delta_H/grinding_freq;
    H_curr = H_curr + delta_H_monthly;
    if(isnan(H_curr))
        H_curr;
    end
    
    % stop if we need to renew the rail or if we are beyond the maximal gauge limit
    % include remaining_lifetime using max_lifetime (from risk tables)
    if(H_curr>H_max || lifetime_remainder <= 0)
        rail_lifetime = m/12; % return lifetime in years
        break;
    end

    % Tamping and its costs
    if(latest_tamping_since==tamping_freq) % time to do tamping
        maintenance = maintenance + tamping_cost_per_meter*track_length_meter/(1+discount_rate)^y;
        train_op = train_op + poss_tamping*cost_hourly_poss/(1+discount_rate)^y;
        gauge_curr = gauge(1);
        latest_tamping_since = 0;
        %lifetime_remainder = lifetime_remainder + interp1(gauge, max_lifetime, gauge_curr, 'linear');
    end
    
    if(gauge_curr>=1450)
        remaining_m = 0;
    end
            
    % Grinding and its costs
    if(latest_grinding_since==grinding_freq) % time to do grinding
        maintenance = maintenance + grinding_cost_per_meter*track_length_meter/(1+discount_rate)^y; 
        latest_grinding_since = 0;
        train_op = train_op + poss_grinding*cost_hourly_poss/(1+discount_rate)^y;
        next_m_grinding = m + grinding_freq;
        % find the increase in gauge when grinding next time
        nb_m = mod(next_m_grinding-1, tamping_freq)+1;
        gauge_grinding = gauge(1) + avg_yearly_gauge_widening/12*nb_m;
        % if gauge is too wide (risk for derailement!)        
        if(gauge_grinding>=1450)
            remaining_m = 0;%(1455-gauge_curr)/(avg_yearly_gauge_widening/12);
            remaining_m = remaining_m + interp1(gauge, max_lifetime, gauge_grinding, 'linear');
            rail_lifetime = (m+remaining_m)/12;
            % grinding lefts, if any!
            if(remaining_m>=grinding_freq)
                nb_grindings_left = fix(remaining_m/grinding_freq);
                maintenance = maintenance + nb_grindings_left*grinding_cost_per_meter*track_length_meter/(1+discount_rate)^y; 
                train_op = train_op + nb_grindings_left*poss_grinding*cost_hourly_poss/(1+discount_rate)^y;
            end
            break;
        end
    end
    
    % older grindng and tamping
    latest_grinding_since = latest_grinding_since + 1; % in months
    latest_tamping_since = latest_tamping_since + 1; % in months
    
end

% after end of track life, get the remaining residual from last renewal
end_of_life = 0;%-get_renewal_cost(track_lifetime_years, inner_rail)*(rail_lifetime-mod(track_lifetime_years,rail_lifetime))/rail_lifetime;

% total LCC in NPV/meter
lcc_total = train_op +maintenance+renewal+end_of_life;
%lcc_total = lcc_total/track_length_meter/track_lifetime_years;
lcc_total = lcc_total/track_length_meter/rail_lifetime;
end


function rc = get_renewal_cost(it_year, inner_rail)

discount_rate = 0.035;

% Track parameters
track_length_meter = 1000; 

% Renewal cost (Material + Work) in SEK per meter
material_work_cost = 1500;%500+924.4;%; 
% if(strcmp(inner_rail,"MB6"))
%     material_work_cost =2214;  %500+924.7;% 
% end

% total renewl cost
rc = material_work_cost*track_length_meter/(1+discount_rate)^it_year;

end