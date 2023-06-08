function [annuity, TPV] = get_ann_tpv(dir_maint, prev_cap, korr_cap, disr, renewal_costs_switches)
%GET_ANN given the life cycle yearly costs, calculate the annuity

time_horizon = size(dir_maint,1);
nb_switches = size(dir_maint,2);

% Compute the sum of undiscounted costs
total_cost = dir_maint + prev_cap + korr_cap + disr;

% % Compute the percentage of different costs over all years for each switch type
% total_cost_yearly = sum(dir_maint, 1) + sum(prev_cap, 1) + sum(korr_cap, 1) + sum(disr, 1);
% perc_dir_maint = (sum(dir_maint, 1) ./ total_cost_yearly) * 100
% perc_prev_cap = (sum(prev_cap, 1) ./ total_cost_yearly) * 100
% perc_korr_cap = (sum(korr_cap, 1) ./ total_cost_yearly) * 100
% perc_disr = (sum(disr, 1) ./ total_cost_yearly) * 100

% discouting
rate=.035;

% % % variant 1
% total_discounted_cost = total_cost;
% for sw =1:nb_switches
%     for y=1:time_horizon
%             total_discounted_cost(y,sw) = total_cost(y,sw)/(1+rate)^y;
%     end
% end
% TPV = sum(total_discounted_cost,1)+renewal_costs_switches'; % first renewal is added
% annuity = TPV/time_horizon;

% variant 2
year_lifetime = 75;
total_discounted_cost = zeros(year_lifetime,nb_switches);
residual = zeros(nb_switches,1);
for sw =1:nb_switches
    y_since_renewal = 0;
    for y=1:year_lifetime
        y_since_renewal = y_since_renewal + 1;
        if(y_since_renewal==time_horizon) % time for renewal
            total_discounted_cost(y,sw) = (total_cost(y_since_renewal,sw)+renewal_costs_switches)/(1+rate)^y;
            y_since_renewal = 0;
        else
            total_discounted_cost(y,sw) = total_cost(y_since_renewal,sw)/(1+rate)^y;
        end
    end
    residual(sw) = - renewal_costs_switches*(time_horizon-y_since_renewal)/time_horizon;
    residual(sw) = residual(sw)/(1+rate)^year_lifetime; % discounting
end
TPV = sum(total_discounted_cost,1)+ renewal_costs_switches'+residual'; % first renewal is added
%annuity = TPV/year_lifetime;
annuity = TPV.*(rate*(1+rate).^year_lifetime')./((1+rate).^year_lifetime'-1); % ./year_lifetime';


end

