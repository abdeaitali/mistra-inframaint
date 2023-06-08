function [dir_maint_cost,prev_cap_cost,korr_cap_cost,disruption_cost] = assess_lcc(data)
%ASSESS_LCC given corrective and preventive and failure tables, calculate
%the social costs over the life cycle of the switch
prev = data{1};
korr = data{2};
fail = data{3};
nb_freight_year = data{4};
nb_pass_year = data{5};
delay_min = data{6};
time_horizon = data{7};
headers = data{8};
% maintenance work costs
korr_main_cost = data{9};%8000; % sek per activity, 2014-price level
prev_main_cost = data{10};%5000; % sek per activity, 2014-price level

% all types of switches and components
nb_headers = length(headers);

% track access time (maintenance windows)
track_access_time_korr = 1; % in hours (immediate, possibly anytime)
track_access_time_prev = 4; % in hours (mainly night-times)

% MGT annual traffic
MGT_year = 8; % fixed for all types

% average train loads (in tons or persons)
avg_ton_freight = 400;
avg_pass_intercity = 241;
avg_pass_commuter = 131;

% train path cost data
%  kr per person/ton-km (ref. trafikanalys) https://www.trafa.se/globalassets/pm/2023/pm-2023_1-transportsektorns-samhallsekonomiska-kostnader-2022---bilagor.pdf
freight_path_unit_cost =.00779;%kr per ton-km
intercity_path_unit_cost = .05813;%kr per pax-km
commuter_path_unit_cost = .05813;%kr per pax-km
% average travel distance assumumption 100/300/400 km
freight_path_cost =46350;%400*avg_ton_freight*freight_path_unit_cost;%46350;% sek per train path
intercity_path_cost = 57628;%300*avg_pass_intercity*intercity_path_unit_cost;%57628;%1526; % sek per train path
commuter_path_cost = 29812;%100*avg_pass_commuter*commuter_path_unit_cost;%29812;%2081; % sek per train path


% delay cost data per 
freight_disruption_unit_cost = 3.845; % sek per ton-hour
intercity_disruption_unit_cost = .25*1008.3+.75*298; % sek per person-hour
commuter_disruption_unit_cost = .75*281.7+.25*1008.3; % sek per person-hour
% - per train
freight_disruption_cost = avg_ton_freight*freight_disruption_unit_cost; % sek per train-hour
intercity_disruption_cost = avg_pass_intercity*intercity_disruption_unit_cost; % sek per train-hour
commuter_disruption_cost = avg_pass_commuter*commuter_disruption_unit_cost; % sek per train-hour

% preventiva underhållsåtgärder
nb_prev = 14;
limit_load_prev = [65 400 400 50 90 100 200 8 40 200 100 50 200 200];
kostnad_prev = [50000 350000 350000 30000 200000 300000 60000 4000 12000 200000 30000 15000 125000 40000];

% init
korr_cap_cost = zeros(time_horizon,nb_headers);
prev_cap_cost = zeros(time_horizon,nb_headers);
disruption_cost = zeros(time_horizon,nb_headers);
dir_maint_cost = zeros(time_horizon,nb_headers);


for h=1:nb_headers % all switch types (or ERS levels, if ERS=1)
    accumulated_load_prev = zeros(1,nb_prev);
    for y=1:time_horizon
        
        % direct maintenance costs
        dir_maint_cost(y,h) = dir_maint_cost(y,h) + korr(y, h)*korr_main_cost;
        dir_maint_cost(y,h) = dir_maint_cost(y,h) + prev(y, h)*prev_main_cost;
        
        % preventive capacity costs (done mainly during the nights where mostly freight traffic)
        accumulated_load_prev(:) = accumulated_load_prev(:) + MGT_year;
        nb_prev_activities = prev(y, h);
        for p=1:nb_prev
            if(accumulated_load_prev(p)>=limit_load_prev(p)) % for switches, att efter 90 MBT är en av de förebyggande åtgärderna
                % ett komponentutbyte av en tunganordningshalva, och att efter 100 MBT
                % är en av de förebyggande åtgärderna ett komponentbyte av en korsning
                dir_maint_cost(y,h) = dir_maint_cost(y,h)+kostnad_prev(p);
                accumulated_load_prev(p) = accumulated_load_prev(p)-limit_load_prev(p);
               %   nb_prev_activities = nb_prev_activities + 1;
            end
        end
        nb_freight_paths = nb_prev_activities*track_access_time_prev*nb_freight_year(h)/365/24;
        prev_cap_cost(y,h) = freight_path_cost*nb_freight_paths;
        
        % corr (done immediately/day)
        nb_korr_activities = korr(y, h);
        if(mod(y,8)==0) % Växelvärmeelement, byte (baseras på 16 element, ofta som avhjälpande underhåll) 
            dir_maint_cost(y,h) = dir_maint_cost(y,h) + 50000;
%               nb_korr_activities = nb_korr_activities + 1;
        end
        nb_train_year = nb_freight_year(h)+nb_pass_year(h);
        nb_train_paths = nb_korr_activities*track_access_time_korr*nb_train_year/365/24;
        unit_cost = nb_freight_year(h)*freight_path_cost+nb_pass_year(h)*(intercity_path_cost+commuter_path_cost)/2;
        unit_cost = unit_cost/nb_train_year;
        korr_cap_cost(y,h) = unit_cost*nb_train_paths;
    
        % disruption costs
        delay_hour = fail(y, h)*delay_min(h)/nb_train_year/60;
        unit_cost = nb_freight_year(h)*freight_disruption_cost+nb_pass_year(h)*(intercity_disruption_cost+commuter_disruption_cost)/2;
%          unit_cost = 1200*60;
        disruption_cost(y,h) = delay_hour*unit_cost;
    end
    
end
end