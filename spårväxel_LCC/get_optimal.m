function [optimal_lifetime_switches, min_annuity_switches, annuity_switches] = get_optimal(data_lcc, time_horizon_switches_max, headers_switches, renewal_costs_switches)
%GET_OPTIMAL Summary of this function goes here
%   Detailed explanation goes here

% Annuity for different lifetimes
nb_headers = size(headers_switches,1);
annuity_switches = zeros(time_horizon_switches_max,nb_headers);
tpv = zeros(time_horizon_switches_max,nb_headers);
[dir_maint,prev_cap,korr_cap,disr] = assess_lcc(data_lcc);
for y=1:time_horizon_switches_max
    [annuity_switches(y,:), tpv(y,:)] = get_ann_tpv(dir_maint(1:y,:), prev_cap(1:y,:), korr_cap(1:y,:), disr(1:y,:), renewal_costs_switches);
end

% minimal annuity
[min_annuity_switches, optimal_lifetime_switches] = min(annuity_switches, [], 1);
end

