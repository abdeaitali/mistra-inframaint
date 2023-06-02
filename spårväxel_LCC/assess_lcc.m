function [dir_maint_cost,prev_cap_cost,korr_cap_cost,disruption_cost] = assess_lcc(prev,korr,fail,MGT,nb_freight_year,nb_pass_year,delay_min,time_horizon,headers,ERS)
%ASSESS_LCC given corrective and preventive and failure tables, calculate
%the social costs over the life cycle of the switch

ERS_level = 0;
if nargin < 10 || isempty(ERS)
    ERS = 0; % by default no ERS
elseif(ERS == 1) % ERS calculations
    ERS_level = headers{2};
    headers = headers{1};
end

% all types of switches and components
nb_headers = size(headers,2);

% maintenance work costs
korr_main_cost = 8000; % sek per activity, 2014-price level
prev_main_cost = 10000;%10000; % sek per activity, 2014-price level
inspection_cost = 18000;%18000;%7067; % sek per activity, 2014-price level

% track access time (maintenance windows)
track_access_time_korr = 2; % in hours (immediate, possibly anytime)
track_access_time_prev = 4; % in hours (mainly night-times)

% MGT annual traffic
MGT_year = MGT; % different MGT for different switch types
%MGT_year(:) = 8; % fixed for all types

% average train loads (in tons or persons)
avg_ton_freight = 400;
avg_pass_intercity = 241;
avg_pass_commuter = 131;

% train path cost data
%  kr per person/ton-km (ref. trafikanalys) https://www.trafa.se/globalassets/pm/2023/pm-2023_1-transportsektorns-samhallsekonomiska-kostnader-2022---bilagor.pdf
freight_path_unit_cost =.03086;%kr per ton-km
intercity_path_unit_cost = .09684;%kr per pax-km
commuter_path_unit_cost = .09684;%kr per pax-km
% average travel distance assumumption 100/300/400 km
freight_path_cost =400*avg_ton_freight*freight_path_unit_cost;%10490;% sek per train path
intercity_path_cost = 300*avg_pass_intercity*intercity_path_unit_cost;%25264;%1526; % sek per train path
commuter_path_cost = 100*avg_pass_commuter*commuter_path_unit_cost;%29812;%2081; % sek per train path

% delay cost data per 
freight_disruption_unit_cost = 3.845; % sek per ton-hour
intercity_disruption_unit_cost = .25*1008.3+.75*298; % sek per person-hour
commuter_disruption_unit_cost = .75*281.7+.25*1008.3; % sek per person-hour
% - per train
freight_disruption_cost = avg_ton_freight*freight_disruption_unit_cost; % sek per train-hour
intercity_disruption_cost = avg_pass_intercity*intercity_disruption_unit_cost; % sek per train-hour
commuter_disruption_cost = avg_pass_commuter*commuter_disruption_unit_cost; % sek per train-hour

% init
korr_cap_cost = zeros(time_horizon,nb_headers);
prev_cap_cost = zeros(time_horizon,nb_headers);
disruption_cost = zeros(time_horizon,nb_headers);
dir_maint_cost = zeros(time_horizon,nb_headers);


for h=1:nb_headers
    type = headers(h);
    accumulated_load_tunganordningshalva = 0;
    accumulated_load_korsning = 0;
    
    for y=1:time_horizon
        
        % preventive capacity costs (done mainly during the nights where mostly freight traffic)
        accumulated_load_tunganordningshalva = accumulated_load_tunganordningshalva + MGT_year(h);
        accumulated_load_korsning = accumulated_load_korsning + MGT_year(h);
        nb_prev_activities = prev(y, type);
        if(accumulated_load_tunganordningshalva>=90) % for switches, att efter 90 MBT är en av de förebyggande åtgärderna
            % ett komponentutbyte av en tunganordningshalva, och att efter 100 MBT
            % är en av de förebyggande åtgärderna ett komponentbyte av en korsning
            dir_maint_cost(y,h) = dir_maint_cost(y,h)+300000;
            accumulated_load_tunganordningshalva = accumulated_load_tunganordningshalva-90;
            nb_prev_activities = nb_prev_activities + 1;
        end
        if(accumulated_load_korsning>=100)
            dir_maint_cost(y,h) = dir_maint_cost(y,h)+200000;
            accumulated_load_korsning = accumulated_load_korsning-100;
            nb_prev_activities = nb_prev_activities + 1;
        end
        nb_freight_paths = nb_prev_activities*track_access_time_prev*nb_freight_year(h)/365/24;
        prev_cap_cost(y,h) = freight_path_cost*nb_freight_paths;
        
        % direct maintenance costs
        dir_maint_cost(y,h) = dir_maint_cost(y,h) + inspection_cost;
        
        % ERS
        if(ERS == 1 && korr(y, type)*korr_main_cost>ERS_level{h})
            dir_maint_cost(y,h) = dir_maint_cost(y,h) + korr(y, type)*korr_main_cost-ERS_level{h};
        else
            dir_maint_cost(y,h) = dir_maint_cost(y,h) + korr(y, type)*korr_main_cost;
        end
        dir_maint_cost(y,h) = dir_maint_cost(y,h) + nb_prev_activities*prev_main_cost;
        
        % corr (done immediately/day)
        nb_train_year = nb_freight_year(h)+nb_pass_year(h);
        nb_train_paths = korr(y, type)*track_access_time_korr*nb_train_year/365/24;
        unit_cost = nb_freight_year(h)*freight_path_cost+nb_pass_year(h)*(intercity_path_cost+commuter_path_cost)/2;
        unit_cost = unit_cost/nb_train_year;
        korr_cap_cost(y,h) = unit_cost*nb_train_paths;
    
        % disruption costs (using )
        delay_hour = fail(y, type)*delay_min(h)/60;
        unit_cost = nb_freight_year(h)*freight_disruption_cost+nb_pass_year(h)*(intercity_disruption_cost+commuter_disruption_cost)/2;
        unit_cost = unit_cost/nb_train_year;
%         unit_cost = 1200*60;
        disruption_cost(y,h) = delay_hour*unit_cost;
    end
    
end
end