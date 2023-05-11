function [nb_grinding,nb_tamping, LCC] = get_optimal(H_table_interpol, interpolation_method, MB, avg_gauge_widening, risk)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here


% simulation
months = 1:12;
simulation_LCC = zeros(months(end),months(end));
for grinding_freq=months
    for tamping_freq=months
        maint_strategy = [grinding_freq,tamping_freq];
        simulation_LCC(grinding_freq,tamping_freq) = get_lcc(H_table_interpol, maint_strategy, interpolation_method, MB, avg_gauge_widening, risk);
    end
end

% find the min
[row_grinding,col_tamping] = find(simulation_LCC==min(simulation_LCC(:)));
nb_grinding = 12/row_grinding(1);
nb_tamping = 12/col_tamping(1);
LCC = min(simulation_LCC(:));


end

