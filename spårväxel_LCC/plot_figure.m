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

elseif(strcmp(type, "annuity") || strcmp(type, "annuity-ERS"))
    annuity_switches = data{1};
    headers = data{2};
    if(strcmp(type, "annuity-ERS"))
        for i=1:length(headers)
            headers{i} = num2str(headers{i});
        end
    end
    time_horizon = size(annuity_switches, 1);
    plot(1:time_horizon, annuity_switches)
    legend(headers, "Location","best")
    xlabel("Lifetime (in years)")
    ylabel("Annuity (SEK per year)")
elseif(strcmp(type, "input") || strcmp(type, "input-ERS"))
    % Access and process the data inside the plot_figure function
    prev = data{1};
    korr = data{2};
    fail = data{3};
    headers_switches = data{4};
    if(strcmp(type, "input-ERS"))
        for i=1:length(headers_switches)
            headers_switches{i} = num2str(headers_switches{i});
        end

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
    
elseif(strcmp(type, "optimal-lifetime") || strcmp(type, "optimal-lifetime-ERS"))
    optimal_lifetime_switches = data{1};
    min_annuity_switches = data{2};
    headers  = data{3};
    if(strcmp(type, "optimal-lifetime-ERS"))
        for i=1:length(headers)
            headers{i} = num2str(headers{i});
        end
    end
    % Create a figure with two y-axes
    figure;
    
    % Set the switch types
    nb_headers= 1:length(headers);
    
    % Define the bar width and spacing
    bar_width = 0.25;  % Adjust the bar width as desired
    bar_spacing = 0.3;  % Adjust the spacing between bars as desired
    
    % Plot the optimal lifetime (blue bars)
    yyaxis left;
    bar(nb_headers - bar_spacing/2, optimal_lifetime_switches, bar_width, 'b');
    ylabel('Optimal Lifetime');
    
    hold on;
    
    % Plot the minimal annuity (red bars)
    yyaxis right;
    bar(nb_headers + bar_spacing/2, min_annuity_switches, bar_width, 'r');
    ylabel('Minimal Annuity (SEK/year)');
    
    % Set the x-axis ticks and labels
    xticks(nb_headers);
    xticklabels(headers);
    xtickangle(45);
    if(strcmp(type, "optimal-lifetime"))
        xlabel('Switch Type');
    else
        xlabel('Level of Reimbursement Rule (in SEK)');
    end    
    
    
    % Adjust y-axis limits for optimal lifetime
    ylim_left = [0, max(optimal_lifetime_switches) * 1.1];  % Adjust the scale factor accordingly
    
    % Set y-axis limits
    yyaxis left;
    ylim(ylim_left);
    ytickformat('%g');
    
    % Set legend
    legend('Optimal Lifetime', 'Minimal Annuity', 'Location', 'bestoutside');
    hold off;
        
elseif(strcmp(type, "break-even"))
    figure;
    min_annuity = data{1};
    headers_num = data{2};
    headers = headers_num;
    for i=1:length(headers_num)
        headers{i} = num2str(headers_num{i});
    end
    
    contract_years = data{3};
    korr_ERS = data{4};
    optimal_lifetime_switches = data{5};
    
    % plot the LCC over the contract period
    plot(1:length(headers), contract_years*min_annuity./optimal_lifetime_switches);
    hold on;
    
    % plot the RR cost per year
    RR = zeros(length(headers),1);
    for h=1:length(headers)
        for y=1:optimal_lifetime_switches(h)
            RR(h) = RR(h) + korr_ERS(y,h)*headers_num{h};
        end
    end
    plot(1:length(headers),contract_years*RR./optimal_lifetime_switches)
    xticklabels(headers);
    legend('LCC','RR')
    hold off;
end

end

