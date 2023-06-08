function plot_figure(type, data)
%PLOT_FIGURE Summary of this function goes here
%   Detailed explanation goes here

if(strcmp(type, "yearly undiscounted")) % LCC for different switch types: Yearly cummulative costs
    % Access and process the data inside the plot_figure function
    dir_maint = data{1};
    prev_cap = data{2};
    korr_cap = data{3};
    disr = data{4};
    %renewal_costs_switches = data{5};
    headers_switches = data{6};
    time_horizon = size(dir_maint,1);
    
    % Compute the sum of costs
    %total_cost = dir_maint + prev_cap + korr_cap + disr;
    %total_cost(end,:) = total_cost(end,:) + renewal_costs_switches';
    
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

elseif(strcmp(type, "input") || strcmp(type, "input-ERS"))
    % Access and process the data inside the plot_figure function
    prev = data{1};
    korr = data{2};
    fail = data{3};
    headers_switches = data{4};
    if(strcmp(type, "input-ERS"))
        headers_switches = num2str(headers_switches{:});
    end
    time_horizon = size(prev, 1);
    
    % plot preventive
    figure;
    hold on;
    for i = 1:size(prev, 2)
        plot(1:time_horizon, prev(:, i), 'DisplayName', headers_switches{i});
    end
    legend('Location', 'best');
    xlabel('Year');
    ylabel('Number');
    title('Preventive');
    
    % plot corrective
    figure;
    hold on;
    for i = 1:size(korr, 2)
        plot(1:time_horizon, korr(:, i), 'DisplayName', headers_switches{i});
    end
    legend('Location', 'best');
    xlabel('Year');
    ylabel('Number');
    title('Corrective');
    
    % plot delays
    figure;
    hold on;
    for i = 1:size(fail, 2)
        plot(1:time_horizon, fail(:, i), 'DisplayName', headers_switches{i});
    end
    legend('Location', 'best');
    xlabel('Year');
    ylabel('Number');
    title('Delays');
    
    hold off;
    
elseif(strcmp(type, "optimal-lifetime"))
    
    switches = data{1};
    optimal_lifetime_switches = data{2};
    min_annuity_switches = data{3};
    headers_switches  = data{4};
    
    % Create a figure with two y-axes
    figure;
    
    % Set the switch types
    switch_types = 1:length(switches);
    
    % Define the bar width and spacing
    bar_width = 0.25;  % Adjust the bar width as desired
    bar_spacing = 0.3;  % Adjust the spacing between bars as desired
    
    % Plot the optimal lifetime (blue bars)
    yyaxis left;
    bar(switch_types - bar_spacing/2, optimal_lifetime_switches, bar_width, 'b');
    ylabel('Optimal Lifetime');
    
    hold on;
    
    % Plot the minimal annuity (red bars)
    yyaxis right;
    bar(switch_types + bar_spacing/2, min_annuity_switches, bar_width, 'r');
    ylabel('Minimal Annuity (SEK/year)');
    
    % Set the x-axis ticks and labels
    xticks(switch_types);
    xticklabels(headers_switches);
    xtickangle(45);
    xlabel('Switch Type');
    
    % Adjust y-axis limits for optimal lifetime
    ylim_left = [0, max(optimal_lifetime_switches) * 1.1];  % Adjust the scale factor accordingly
    
    % Set y-axis limits
    yyaxis left;
    ylim(ylim_left);
    ytickformat('%g');
    
    % Set legend
    legend('Optimal Lifetime', 'Minimal Annuity', 'Location', 'bestoutside');
    
end

end

