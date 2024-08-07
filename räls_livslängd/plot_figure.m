function plot_figure(wanted_fig, arg)
%PLOT_FIGURE Function for plotting figures
%   Depending on input argument, plot specific figures

% gauge intervals (in mm)
gauge = [1440,1445,1450,1455];

% months
months = linspace(1,12,12);

figure
if(strcmp(wanted_fig,'H_table'))
    % visualize the H_table
    plot(months, arg(1,:), 'LineStyle',"-")
    hold on
    plot(months, arg(2,:), 'LineStyle',"--")
    plot(months, arg(3,:), 'LineStyle',"-.")
    plot(months, arg(4,:), 'LineStyle',":")
    legend('1440','1445','1450','1455','Location',"northwest")
    xlabel('Months')
    ylabel('{\it H}-index')
elseif(strcmp(wanted_fig,'H_tables_heatmap'))
    H_table_MB5 = arg{1};
    H_table_MB6 = arg{2};
    
    % Plot the first heat map
    subplot(1, 2, 1);
    [X1, Y1] = meshgrid(months, gauge);
    surf(X1, Y1, H_table_MB5)
    xlabel('Months (since last grinding)')
    ylabel('Gauge (in mm)')
    zlabel('{\it H}-index (increase)')
    
    % Modify font size and tick labels for the first heat map
    set(gca, 'FontSize', 12)
    set(gca, 'TickLabelInterpreter', 'none')
    set(gca, 'YDir', 'reverse')
    
    % Set the same color axis limits for both heat maps
    caxis([min(H_table_MB5(:)), max(H_table_MB6(:))])
    
    % Plot the second heat map
    subplot(1, 2, 2);
    [X2, Y2] = meshgrid(months, gauge(3:4));
    surf(X2, Y2, H_table_MB6)
    xlabel('Months (since last grinding)')
    ylabel('Gauge (in mm)')
    zlabel('{\it H}-index (increase)')
    
    % Modify font size and tick labels for the second heat map
    set(gca, 'FontSize', 12)
    set(gca, 'TickLabelInterpreter', 'none')
    set(gca, 'YDir', 'reverse')

elseif(strcmp(wanted_fig,'H_table5_heatmap'))
    % as a heat map
    [X,Y] = meshgrid(months,gauge);
    surf(X,Y,arg)
    colorbar
    xlabel('Months (since last grinding)')
    ylabel('Gauge (in mm)')
    zlabel('{\it H}-index (increase)')
    title('Maintenance table for MB5-H350LTH (inner rail)')
elseif(strcmp(wanted_fig,'H_table6_heatmap'))
    % as a heat map
    [X,Y] = meshgrid(months,gauge(3:4));
    surf(X,Y,arg)
    colorbar
    xlabel('Months (since last grinding)')
    ylabel('Gauge (in mm)')
    zlabel('{\it H}-index (increase)')    
    title('Maintenance table for MB6-R400HT (inner rail)')
elseif(strcmp(wanted_fig(1:end-4),'LCC_heatmap'))
    % visualize the interpolated H_tables as a heatmap
    % as a heat map
    [nb_months_grinding,nb_months_tamping] = size(arg);
    months_grinding = linspace(1,nb_months_grinding,nb_months_grinding);
    months_tamping = linspace(1,nb_months_tamping,nb_months_tamping);
    
    [X,Y] = meshgrid(months_tamping,months_grinding);
    surf(X,Y,arg)
    colorbar
    ylabel('Grinding interval (in months)','Rotation',-30)
    xlabel('Gauge correction interval (in months)','Rotation',20)
    zlabel('Annuity per meter (in SEK/year)')
    title(append('Annuity of different maintenance strategies for ',wanted_fig(end-2:end)))
elseif(strcmp(wanted_fig,'LCC_heatmaps'))
    
    LCC_MB5 = arg{1};
    LCC_MB6 = arg{2};
    
    % Plot the first heat map
    subplot(1, 2, 1);
    [X1, Y1] = meshgrid(months, months);
    surf(X1, Y1, LCC_MB5)
    xlabel({'Gauge correction interval';'(in months)'},'Rotation',20)
    ylabel({'Grinding interval';'(in months)'},'Rotation',-30)
    zlabel('Total LCC (in SEK/meter)')
    
    % Modify font size and tick labels for the first heat map
    set(gca, 'FontSize', 12)
    set(gca, 'TickLabelInterpreter', 'none')
    set(gca, 'YDir', 'reverse')
    
    % Set the same color axis limits for both heat maps
    caxis([min(LCC_MB5(:)), max(LCC_MB6(:))])
    
    % Plot the second heat map
    subplot(1, 2, 2);
    [X2, Y2] = meshgrid(months, months);
    surf(X2, Y2, LCC_MB6)
    xlabel({'Gauge correction interval';'(in months)'},'Rotation',20)
    ylabel({'Grinding interval';'(in months)'},'Rotation',-30)
    zlabel('Total LCC (in SEK/meter)')
    
    % Modify font size and tick labels for the second heat map
    set(gca, 'FontSize', 12)
    set(gca, 'TickLabelInterpreter', 'none')
    set(gca, 'YDir', 'reverse')

elseif(strcmp(wanted_fig,'interpolation'))
    % visualize the interpolated H_tables
    figure
    plot(months, arg(1,:), 'LineStyle',"-")
    hold on
    plot(months, arg(2,:), 'LineStyle',"--")
    plot(months, arg(3,:), 'LineStyle',"-.")
    plot(months, arg(4,:), 'LineStyle',":")
    legend('1440','1445','1450','1455','Location',"northwest")
    set(gca, 'FontSize', 12)
    xlabel('Months')
    ylabel('{\it H}-index')
elseif(strcmp(wanted_fig(end-12:end),'interpolation'))
    % visualize the interpolated H_tables as a heatmap
    % as a heat map
    if(size(arg,1)==2)
        gauge = gauge(3:4);
    end
    [~,nb_months] = size(arg);
    months = linspace(1,nb_months,nb_months);
    [X,Y] = meshgrid(months,gauge);
    surf(X,Y,arg)
    colorbar
    xlabel('Months (since last grinding)')
    ylabel('Gauge (in mm)')
    zlabel('{\it H}-index (interpolated increase)')
    title(wanted_fig)
    %%% visualize average monthly deterioration in H-index
    figure
    x=[1:nb_months;1:nb_months;1:nb_months;1:nb_months];
    y = arg./x;
    surf(y)
    xlabel('Months (since last grinding)')
    ylabel('Gauge (in mm)')
    zlabel('Monthly increase in {\it H}-index')
elseif(strcmp(wanted_fig, 'sensitivity analysis - gauge widening'))
    
    opt_grinding = arg{1};
    opt_tamping = arg{2};
    ANNs = arg{3};
    lifetimes = arg{4};
    
    % Define the initial gauge widening values
    gauge_widening_values = [1, 2, 3]; % in mm/y
    
    % Plot the variation of optimal lifetimes and ANNs as bar charts
    figure;
    yyaxis left;
    bar(gauge_widening_values, lifetimes, 0.2, 'FaceColor', 'b');
    ylabel('Optimal Lifetime');
    yyaxis right;
    bar(gauge_widening_values + 0.3, ANNs, 0.2, 'FaceColor', 'r');
    ylabel('Annuity (SEK per year and meter)');
    xlabel('Initial gauge widening (mm/y)');
    grid on;
    legend({'Optimal Lifetime', 'ANN'}, 'Location', 'bestoutside');
    
    % Plot the variation of optimal grinding and tamping intervals as bar charts
    figure;
    yyaxis left;
    bar(gauge_widening_values, opt_grinding, 0.2, 'FaceColor', 'b');
    ylabel('Optimal Grinding Interval (months)');
    yyaxis right;
    bar(gauge_widening_values + 0.3, opt_tamping, 0.2, 'FaceColor', 'r');
    ylabel('Optimal Tamping Interval (months)');
    xlabel('Initial gauge widening (mm/y)');
    grid on;
    legend({'Optimal Grinding Interval', 'Optimal Tamping Interval'}, 'Location', 'bestoutside');
    
elseif(strcmp(wanted_fig, 'sensitivity analysis - renewal costs'))
    
    opt_grinding = arg{1};
    opt_tamping = arg{2};
    ANNs = arg{3};
    lifetimes = arg{4};
    rc = arg{5};
    
    % Plot the variation of optimal lifetimes and ANNs
    figure;
    yyaxis left;
    plot(rc, lifetimes, '-o', 'Color', 'b', 'LineWidth', 2);
    ylabel('Optimal Lifetime (years)');
    yyaxis right;
    plot(rc, ANNs, '-x', 'Color', 'r', 'LineWidth', 2);
    ylabel('Annuity (SEK per year and meter)');
    xlabel('Renewal Costs (SEK per meter)');
    grid on;
    legend({'Optimal Lifetime', 'ANN'}, 'Location', 'bestoutside');
    
    % Plot the variation of optimal grinding and tamping intervals
    figure;
    yyaxis left;
    plot(rc, opt_grinding, '-o', 'Color', 'b', 'LineWidth', 2);
    ylabel('Optimal Grinding Interval (months)');
    yyaxis right;
    plot(rc, opt_tamping, '-x', 'Color', 'r', 'LineWidth', 2);
    ylabel('Optimal Tamping Interval (months)');
    xlabel('Renewal Costs (SEK per meter)');
    grid on;
    legend({'Optimal Grinding Interval', 'Optimal Tamping Interval'}, 'Location', 'bestoutside');
    
    
elseif(strcmp(wanted_fig, 'sensitivity analysis - renewal costs & gauge widening'))
    
    ANNs = arg{1};
    lifetimes = arg{2};
    rc = arg{3};
    
    %%% Define variables for plotting
    renewal_costs = rc;
    gauge_widening_labels = {'Gauge Widening from 1mm/y', 'Gauge Widening from 2mm/y', 'Gauge Widening from 3mm/y'};
    colors = {'b', 'g', 'r'};
    
    %%% plot the minimal annuity
    % Plot ANN vs Renewal Costs
    figure;
    hold on;
    for gw = 1:nb_gauge_widening
        plot(renewal_costs, ANNs(:, gw), 'DisplayName', gauge_widening_labels{gw}, 'Color', colors{gw}, 'Marker', 'o');
    end
    xlabel('Renewal Costs');
    ylabel('Minimal annuity (SEK per year and meter)');
    title('ANN vs Renewal Costs for Different Gauge Widenings');
    legend show;
    grid on;
    hold off;
    
    %%% plot the lifetime
    % Plot Lifetime vs Renewal Costs
    figure;
    hold on;
    for gw = 1:nb_gauge_widening
        plot(renewal_costs, lifetimes(:, gw), 'DisplayName', gauge_widening_labels{gw}, 'Color', colors{gw}, 'Marker', 'o');
    end
    xlabel('Renewal Costs (SEK per meter)');
    ylabel('Optimal lifetime (in years)');
    title('Lifetime vs Renewal Costs for Different Gauge Widenings');
    legend show;
    grid on;
    hold off;
    
end

end

