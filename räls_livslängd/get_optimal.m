function [nb_grinding,nb_tamping, LCC, rail_lifetime] = get_optimal(H_table_interpol, interpolation_method, MB, avg_gauge_widening, max_lifetime)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here


% simulation
months = 1:12;
simulation_LCC = zeros(months(end),months(end));
simulation_lifetime = zeros(months(end),months(end));
for grinding_freq=months
    for tamping_freq=months
        maint_strategy = [grinding_freq,tamping_freq];
        [simulation_LCC(grinding_freq,tamping_freq),simulation_lifetime(grinding_freq,tamping_freq)] = get_lcc(H_table_interpol, maint_strategy, interpolation_method, MB, avg_gauge_widening, max_lifetime);
    end
end

% find the min
[row_grinding,col_tamping] = find(simulation_LCC==min(simulation_LCC(:)));
nb_grinding = 12/max(row_grinding(:));
nb_tamping = 12/max(col_tamping(:));
LCC = min(simulation_LCC(:));
rail_lifetime = simulation_lifetime(row_grinding(1), col_tamping(1));
end

