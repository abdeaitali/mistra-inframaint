function [res_lcc, annuity] = assess_lcc(prev,korr,time_horizon,renewal_cost, headers)
%ASSESS_LCC Summary of this function goes here
%   Detailed explanation goes here

% all types of switches and components
nb_types = size(headers,2);

grinding_cost = 54422; % sek per activity, 2014-price level
tamping_cost = 36281; % sek per activity, 2014-price level
inspection_cost = 7067; % sek per activity, 2014-price level
dir_maint_cost = zeros(time_horizon,nb_types);

track_access_time_korr = 1; % in hours (immediate/day)
track_access_time_prev = 4; % in hours (mainly nights)
traffic_night = 10; % trains per 24h (only freight)
yearly_traffic_passenger = 17000; % trains per year (only passenger)
freight_path_cost = 42084; % sek per train path
intercity_path_cost = 123819; % sek per train path
commuter_path_cost = 27628; % sek per train path
korr_cap_cost = zeros(time_horizon,nb_types);
prev_cap_cost = zeros(time_horizon,nb_types);

freight_disruption_cost = 3340; % sek per failure
intercity_disruption_cost = 101076; % sek per failure
commuter_disruption_cost = 45745; % sek per failure
disruption_cost = zeros(time_horizon,nb_types);

for type=1:nb_types
    
    %% direct maintenance costs
    for y=1:time_horizon
        % discounting missing!
        nb_activities = prev(y, type) + korr(y, type);
        dir_maint_cost(y,type) = inspection_cost + nb_activities*(tamping_cost+grinding_cost)/2;
    end
    
    %% capacity costs
    for y=1:time_horizon
        % prev (done mainly during the nights where mostly freight traffic)
        nb_prev_activities = prev(y, type);
        nb_freight_paths = nb_prev_activities*track_access_time_prev*traffic_night/24;
        prev_cap_cost(y,type) = freight_path_cost*nb_freight_paths;
        % corr (done immediately/day)
        nb_korr_activities = korr(y, type);
        nb_freight_paths = nb_korr_activities*track_access_time_korr*traffic_night/24;
        nb_pass_paths = nb_korr_activities*track_access_time_korr*.5*yearly_traffic_passenger/(365*24);
        korr_cap_cost(y,type) = freight_path_cost*nb_freight_paths+nb_pass_paths*(intercity_path_cost+commuter_path_cost);
    end
    
    %% disruption costs
    for y=1:time_horizon
        nb_korr_activities = korr(y, type);
        disruption_cost(y,type) = nb_korr_activities*(freight_disruption_cost+intercity_disruption_cost+commuter_disruption_cost);
    end
    
end

%% undiscounted total & annuity
% total (undiscounted)
lcc_undiscounted =  disruption_cost + korr_cap_cost + prev_cap_cost + dir_maint_cost;
lcc_undiscounted(1,:) = lcc_undiscounted(1,:) + renewal_cost';
% annuity
rate=.04;
annuity = sum(lcc_undiscounted,1)*(rate/(1 -(1 + rate)^(-time_horizon)));

%% discouting
res_lcc = zeros(size(lcc_undiscounted));
for y=1:time_horizon
    res_lcc(y,:) = lcc_undiscounted(y,:)/(1+rate)^y;
end
end
