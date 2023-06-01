function [annuity, TPV] = get_ann_tpv(dir_maint, prev_cap, korr_cap, disr, renewal_costs_switches, year_lifetime)
%GET_ANN given the life cycle yearly costs, calculate the annuity

time_horizon = size(dir_maint,1);
nb_switches = size(dir_maint,2);

% Compute the sum of undiscounted costs
total_cost = dir_maint + prev_cap + korr_cap + disr;
%total_cost(end,:) = total_cost(end,:) + renewal_costs_switches';
    
% discouting
total_discounted_cost = zeros(max(year_lifetime(:)),nb_switches);
rate=.05;
residual = zeros(nb_switches,1);

for sw =1:nb_switches
    y_since_renewal = 0;
    for y=1:year_lifetime(sw)
        y_since_renewal = y_since_renewal + 1;
        if(y_since_renewal==time_horizon) % time for renewal
            total_discounted_cost(y,sw) = (total_cost(y_since_renewal,sw)+renewal_costs_switches(sw))/(1+rate)^y;
            y_since_renewal = 0;
        else
            total_discounted_cost(y,sw) = total_cost(y_since_renewal,sw)/(1+rate)^y;
        end
    end
    residual(sw) = - renewal_costs_switches(sw)*(time_horizon-y_since_renewal)/time_horizon;
    residual(sw) = residual(sw)/(1+rate)^year_lifetime(sw); % discounting
end

TPV = sum(total_discounted_cost,1)+residual'+ renewal_costs_switches'; % first renewal is added
annuity = TPV.*(rate*(1+rate).^year_lifetime')./((1+rate).^year_lifetime'-1);

end

