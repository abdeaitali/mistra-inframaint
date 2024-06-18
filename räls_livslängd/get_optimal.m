function [nb_grinding,nb_tamping, LCC, rail_lifetime] = get_optimal(H_table_interpol, interpolation_method, MB, avg_gauge_widening, max_lifetime)
%UNTITLED Finds the optimal maintenance strategy and lifetime
%   Given certain inputs (interpolated H-table, gauge widening), the
%   function finds the optimal rail lifetime and the maintenance strategy
%   (grinding & tamping) as well as the corresponding LCCs


% simulation
months = 1:18;
simulation_LCC = zeros(months(12),months(end));
simulation_lifetime = zeros(months(12),months(end));
for grinding_freq=months(1:12)
    for tamping_freq=months
        maint_strategy = [grinding_freq,tamping_freq];
        [simulation_LCC(grinding_freq,tamping_freq),simulation_lifetime(grinding_freq,tamping_freq)] = get_lcc(H_table_interpol, maint_strategy, interpolation_method, MB, avg_gauge_widening, max_lifetime);
    end
end

% find the min
[row_grinding,col_tamping] = find(simulation_LCC==min(simulation_LCC(:))); % grinding/tamping intervals (in months)
nb_grinding = 12/max(row_grinding(:)); % number of grindings per year
nb_tamping = 12/max(col_tamping(:)); % number of tampings per year
LCC = min(simulation_LCC(:)); % minimal LCC
rail_lifetime = simulation_lifetime(row_grinding(1), col_tamping(1)); % optimal rail lifetime
end

