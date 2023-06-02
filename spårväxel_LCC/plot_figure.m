function plot_figure(type, data)
%PLOT_FIGURE Summary of this function goes here
%   Detailed explanation goes here

if(strcmp(type, "yearly undiscounted")) % LCC for different switch types: Yearly cummulative costs
    % Access and process the data inside the plot_figure function
    dir_maint = data{1};
    prev_cap = data{2};
    korr_cap = data{3};
    disr = data{4};
    renewal_costs_switches = data{5};
    headers_switches = data{6};
    time_horizon = size(dir_maint,1);
    
    % Compute the sum of costs
    total_cost = dir_maint + prev_cap + korr_cap + disr;
    total_cost(end,:) = total_cost(end,:) + renewal_costs_switches';
    
    for h=1:size(headers_switches,1)

        % header
        header = headers_switches{h};
        
        % Compute the share of each cost
%         dir_maint_share = dir_maint(:,h) ./ total_cost(:,h);
%         prev_cap_share = prev_cap(:,h) ./ total_cost(:,h);
%         korr_cap_share = korr_cap(:,h) ./ total_cost(:,h);
%         disr_share = disr(:,h) ./ total_cost(:,h);
        
        figure;
        x = 1:time_horizon;
        bar(x, [disr(:,h), korr_cap(:,h),prev_cap(:,h),  dir_maint(:,h)], 'stacked');
        colormap([0 0.4470 0.7410; 0.8500 0.3250 0.0980; 0.9290 0.6940 0.1250; 0.4940 0.1840 0.5560]);
        legend('Disruptions', 'Corrective Capacity','Preventive Capacity', 'Direct Maintenance', 'Location', 'best');
        xlabel('Year');
        ylabel('Yearly Undiscounted Costs (SEK)');
        title(header)
    end

elseif(strcmp(type, "input"))
    % Access and process the data inside the plot_figure function
    prev = data{1};
    korr = data{2};
    fail = data{3};
    headers_switches = data{4};
    time_horizon = size(prev, 1);
    
    % plot preventive
    figure;
    hold on;
    for i = 1:size(prev, 2)
        plot(1:time_horizon, prev(:, i), 'DisplayName', num2str(headers_switches{i}));
    end
    legend('Location', 'best');
    xlabel('Year');
    ylabel('Number');
    title('Preventive');
    
    % plot corrective
    figure;
    hold on;
    for i = 1:size(korr, 2)
        plot(1:time_horizon, korr(:, i), 'DisplayName', num2str(headers_switches{i}));
    end
    legend('Location', 'best');
    xlabel('Year');
    ylabel('Number');
    title('Corrective');
    
    % plot delays
    figure;
    hold on;
    for i = 1:size(fail, 2)
        plot(1:time_horizon, fail(:, i), 'DisplayName', num2str(headers_switches{i}));
    end
    legend('Location', 'best');
    xlabel('Year');
    ylabel('Number');
    title('Delays');    
    
    
    
end

end

