function plot_figure(wanted_fig, arg)
%PLOT_FIGURE Function for plotting figures
%   Depending on input argument, plot specific figures

% gauge intervals (in mm)
gauge = [1440,1445,1450,1455];

% months
months = linspace(1,12,12);

if(strcmp(wanted_fig,'H_table'))
    % visualize the H_table
    figure
    plot(months, arg(1,:), 'LineStyle',"-")
    hold on
    plot(months, arg(2,:), 'LineStyle',"--")
    plot(months, arg(3,:), 'LineStyle',"-.")
    plot(months, arg(4,:), 'LineStyle',":")
    legend('1440','1445','1450','1455','Location',"northwest")
    xlabel('Months')
    ylabel('H-measure')
elseif(strcmp(wanted_fig,'H_table_heatmap'))
    % as a heat map
    [X,Y] = meshgrid(months,gauge);
    surf(X,Y,arg)
    colorbar
    xlabel('Months (since last grinding)')
    ylabel('Gauge in mm')
    zlabel('H-measure (increase)')
elseif(strcmp(wanted_fig,'interpolation'))
    % visualize the interpolated H_tables
    figure
    plot(months, arg(1,:), 'LineStyle',"-")
    hold on
    plot(months, arg(2,:), 'LineStyle',"--")
    plot(months, arg(3,:), 'LineStyle',"-.")
    plot(months, arg(4,:), 'LineStyle',":")
    legend('1440','1445','1450','1455','Location',"northwest")
    xlabel('Months')
    ylabel('H-measure')
elseif(strcmp(wanted_fig,'interpolation_heatmap'))
    % visualize the interpolated H_tables as a heatmap
    % as a heat map
    [X,Y] = meshgrid(months,gauge);
    surf(X,Y,arg)
    colorbar
    xlabel('Months (since last grinding)')
    ylabel('Gauge in mm')
    zlabel('H-measure (interpolated increase)')
    title('Spline interpolation')
end

end

