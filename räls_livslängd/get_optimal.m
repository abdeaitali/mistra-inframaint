function [opt_grinding, opt_tamping, min_ANN, opt_lifetime] = get_optimal(H_interpolated, ...
    NW_interpolated, interpolation_method, gauge_widening, max_lifetime, tamping_freq_max,...
    renewal_costs)
%get_optimal Finds the optimal maintenance strategy and lifetime
%   Given certain inputs (interpolated H-table, gauge widening), the
%   function finds the optimal rail lifetime and the maintenance strategy
%   (grinding & tamping) as well as the corresponding LCCs


%%% initializations
months_tamping = 1:tamping_freq_max; % max number of months before tamping
grinding_freq_max = 12;
months_grinding = 1:grinding_freq_max;
simulation_LCC = zeros(months_grinding(end),months_tamping(end));
rail_lifetime = zeros(months_grinding(end),months_tamping(end));

%%% find the optimal (LCC-minimal) strategies for tamping and grinding
for grinding_freq=months_grinding % different grinding frequencies
    for tamping_freq=months_tamping % different tamping frequencies
        %%% set strategy
        maint_strategy = [grinding_freq,tamping_freq];
%          maint_strategy = [grinding_freq,42];
        %%% calculate LCC (annuity)
        [simulation_LCC(grinding_freq,tamping_freq),rail_lifetime(grinding_freq,tamping_freq)] = ...
            get_lcc(H_interpolated, NW_interpolated, maint_strategy, interpolation_method, ...
            gauge_widening, max_lifetime, renewal_costs);
    end
end

%%% plot the variation of LCC/annuity for different maintenance strategies
% plot_figure('LCC_heatmap MB5', simulation_LCC);

%%% get optimal/minimal annuity
min_ANN = min(simulation_LCC(:));

%%% get the corresponding optimal strategy (or strategies)
[opt_grinding, opt_tamping] = find(simulation_LCC==min_ANN);

%%% get the corresponding optimal rail lifetime
opt_lifetime = rail_lifetime(opt_grinding(1), opt_tamping(1));



%%%%%%%%

% % simulation
% months = 1:18;
% simulation_LCC = zeros(months(12),months(end));
% simulation_lifetime = zeros(months(12),months(end));
% for grinding_freq=months(1:12)
%     for tamping_freq=months
%         maint_strategy = [grinding_freq,tamping_freq];
%         [simulation_LCC(grinding_freq,tamping_freq),simulation_lifetime(grinding_freq,tamping_freq)] = get_lcc(H_table_interpol, maint_strategy, interpolation_method, MB, avg_gauge_widening, max_lifetime);
%     end
% end
% 
% % find the min
% [row_grinding,col_tamping] = find(simulation_LCC==min(simulation_LCC(:))); % grinding/tamping intervals (in months)
% opt_grinding = 12/max(row_grinding(:)); % number of grindings per year
% nb_tamping = 12/max(col_tamping(:)); % number of tampings per year
% LCC = min(simulation_LCC(:)); % minimal LCC
% rail_lifetime = simulation_lifetime(row_grinding(1), col_tamping(1)); % optimal rail lifetime
% end

