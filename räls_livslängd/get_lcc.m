function [lcc_total, rail_lifetime] = get_lcc(H_table, maint_strategy, type, inner_rail, avg_yearly_gauge_widening, max_lifetime)
%GET_LCC calculates the total lifecycle costs
%   Given a maintenance strategy (frequency of tamping/grinding), the
%   function estimates the total LCC in net present value

discount_rate = 0.35;

% Track parameters
track_length_meter = 1000; 
track_lifetime_years = 15;

% Cost parameters
tamping_cost_per_meter = 40;
grinding_cost_per_meter = 50;

% maintenance frequency
grinding_freq = maint_strategy(1);
tamping_freq = maint_strategy(2);

% train operation parameters
nb_daily_trains = 20;
cost_hourly_poss = 50293;

% track possession per activity in hours
poss_grinding = 2;
poss_tamping = 2;
if(strcmp(inner_rail,"MB6"))
    poss_grinding = 3;
end

% gauge intervals (in mm)
gauge = [1440,1445,1450,1455];
Xq = gauge;

% months
months = 1:12;
Yq= months;

% maximum H (criterion for rail renewal)
H_max = 14;

% find the corresponding total LCC 
H_curr = 0;
gauge_curr = 1440;
renewal = get_renewal_cost(0, inner_rail); % initial renewal
maintenance = 0;
train_op = 0;
latest_grinding_since = 0; % in months
latest_tamping_since = 0; % in months
rail_lifetime = 15;
lifetime_remainder = 12;
for m=1:180 % till track lifetime
    
    % convert month to year
    y = ceil(m/12);
    
    % older grindng and tamping
    latest_grinding_since = latest_grinding_since + 1; % in months
    latest_tamping_since = latest_tamping_since + 1; % in months
    
    % gauge increase after X months
    gauge_curr = gauge_curr+ avg_yearly_gauge_widening/12;
    
    % shorter lifetime
    lifetime_remainder = lifetime_remainder - 1;
    row = floor((gauge_curr-1440)/5) + 1;
    lifetime_remainder = max([lifetime_remainder max_lifetime(row)]);
    
    % corresponding increase in H measure
    H_curr = H_curr + interp2(Xq, Yq, H_table(:,Yq)', gauge_curr, latest_grinding_since,type);

    % stop if we need to renew the rail or if we are beyond the maximal gauge limit
    % TO DO! include remaining_lifetime using max_lifetime (from risk tables)
    if(H_curr>=H_max || gauge_curr>1455 || lifetime_remainder ==0)
        renewal = renewal + get_renewal_cost(y, inner_rail);
        if(rail_lifetime == 15)
            rail_lifetime = y;
        end
        H_curr = 0;
        gauge_curr = 1440;
        latest_grinding_since = 0; % in months
        latest_tamping_since = 0; % in months
        lifetime_remainder = 12;
    end
    
    % Grinding and its costs
    if(latest_grinding_since==grinding_freq) % time to do grinding
        maintenance = maintenance + grinding_cost_per_meter*track_length_meter/(1+discount_rate)^y; 
        latest_grinding_since = 0;
        train_op = train_op + poss_grinding*nb_daily_trains/24*cost_hourly_poss/(1+discount_rate)^y;
    end

    % Tamping and its costs
    if(latest_tamping_since==tamping_freq) % time to do tamping
        maintenance = maintenance + tamping_cost_per_meter*track_length_meter/(1+discount_rate)^y;
        train_op = train_op + poss_tamping*nb_daily_trains/24*cost_hourly_poss/(1+discount_rate)^y;
        if(latest_grinding_since == 0) % if done at the same time as grinding, save 50%!
            maintenance = maintenance - 0.5*tamping_cost_per_meter*track_length_meter/(1+discount_rate)^y;
            train_op = train_op - .5*poss_tamping*nb_daily_trains/24*cost_hourly_poss/(1+discount_rate)^y;
        end
        gauge_curr = 1440;
        latest_tamping_since = 0;
    end
end

% after end of track life, get the remaining residual from last renewal
end_of_life = -get_renewal_cost(track_lifetime_years, inner_rail)*(rail_lifetime-mod(track_lifetime_years,rail_lifetime))/rail_lifetime;

% total LCC in NPV/meter
lcc_total = train_op/track_length_meter + (maintenance+renewal+end_of_life)/track_length_meter;
end


function rc = get_renewal_cost(it_year, inner_rail)

discount_rate = 0.35;

% Track parameters
track_length_meter = 1000; 

% Renewal cost (Material + Work) in SEK per meter
material_work_cost = 500+924.4;
if(strcmp(inner_rail,"MB6"))
    material_work_cost = 500+924.7;
end

% total renewl cost
rc = material_work_cost*track_length_meter/(1+discount_rate)^it_year;

end