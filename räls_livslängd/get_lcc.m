function lcc_total = get_lcc(maint_strategy)
%GET_LCC Summary of this function goes here
%   Detailed explanation goes here
outputArg1 = inputArg1;
outputArg2 = inputArg2;

discount_rate = 0.3;

% Track parameters
track_length_meter = 1000; 
track_lifetime_years = 15;

% Cost parameters
tamping_cost_per_meter = 40;
grinding_cost_per_meter = 50;

% maintenance frequency
nb_yearly_grinding = maint_strategy(1);
nb_yearly_tamping = maint_strategy(2);

% train operation parameters
nb_daily_trains = 20;
cost_hourly_poss = 50293;

% track possession per activity in hours
poss_grinding = 2;
poss_tamping = 2;

% init
renewal = get_renewal_cost(0); % initial renewal
maintenance = 0;
train_op = 0;

for y=1:track_lifetime_years
    
    % Grinding costs
    maintenance = maintenance + (nb_yearly_grinding*grinding_cost_per_meter)*track_length_meter/(1+discount_rate)^y; 
    
    % Tamping costs
    maintenance = maintenance + nb_yearly_tamping*tamping_cost_per_meter*track_length_meter/(1+discount_rate)^y; 
    
    % If renewal criterion is reached
    if renewal == 1
        renewal = renewal + get_renewal_cost(y);
        rail_lifetime = y;
    end
    
    % Train operation costs due to grinding
    train_op = train_op + poss_grinding*nb_yearly_grinding*nb_daily_trains/24*cost_hourly_poss/(1+discount_rate)^y;
    % Same due to tamping
    train_op = train_op + poss_tamping*nb_yearly_tamping*nb_daily_trains/24*cost_hourly_poss/(1+discount_rate)^y;
    
end

% after end of track life, get the remaining residual from last renewal
end_of_life = -get_renewal_cost(track_lifetime_years)*(2*rail_lifetime-track_lifetime_years)/rail_lifetime;


% total LCC in NPV/meter
lcc_total = train_op/track_length_meter + (maintenance+renewal+end_of_life)/track_length_meter;

end


function rc = get_renewal_cost(it_year)

discount_rate = 0.3;

% Track parameters
track_length_meter = 1000; 

% Renewal cost (Material + Work) in SEK per meter
material_work_cost = 1500;

% total renewl cost
rc = material_work_cost*track_length_meter/(1+discount_rate)^it_year;

end