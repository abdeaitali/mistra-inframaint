function [table_interpol] = interpolation(table, type, grinding_freq_max, arg_num)
%INTERPOLATION Interpolation of the H-index look-up table
%   Given a specific interpolation method, this function replaces the values
%   of the first months with an interpolation
%   parameter arg_num is 1 if it is natural wear interpolation
%                        0 if it is gauge widening interpolation
%                        -1/else otherwise


%%% the indices of the months

%Yq = [0,7,8,9,10,11,12]; % months. month zero is 1 in the list
Yq = [0,10,11,12];

if(arg_num==1)
    Yq = linspace(0,12,13);% for natural wear, consider all months in the interpolation
end

%Yq = linspace(1,12,12)-1;

%%% the indices of the track gauges (in mm)
gauge = [1440,1445,1450,1455];
if(arg_num==0)
  gauge = table(:,1)';
  table = table(:,2:end);
  Yq = [1,2,3]; % initial gauge widening 1, 2 or 3mm/y
end

%%% initializations
table_interpol = zeros(4,grinding_freq_max);
ext_H_table = [zeros(size(gauge,2),1) table];

if(arg_num == 0)
    table_interpol = zeros(4,3);

    %%% interpolation of the gauge widening
    % Prepare the data for interpolation
    [X, Y] = meshgrid(Yq, gauge);
    V = table(:, Yq);
    
    % Flatten the data for scatteredInterpolant
    X = X(:);
    Y = Y(:);
    V = V(:);
    
    % Create the interpolant
    F = scatteredInterpolant(X, Y, V, type, 'linear');

    % Interpolation and extrapolation 
    std_gauge = [1440,1445,1450,1455];
    for g_id = 1:length(std_gauge) % for each gauge 
        for init_wg = 1:length(Yq) % for each of the three initial widening
            table_interpol(g_id, init_wg) = F(init_wg, std_gauge(g_id));
        end
    end
else
    %%% interpolation of the look-up tables
    % Prepare the data for interpolation
    [X, Y] = meshgrid(Yq, gauge);
    V = ext_H_table(:, Yq + 1);
    
    % Flatten the data for scatteredInterpolant
    X = X(:);
    Y = Y(:);
    V = V(:);
    
    % Create the interpolant
    F = scatteredInterpolant(X, Y, V, type, 'linear');
    
    % Interpolation and extrapolation for each month and gauge
    for g_id = 1:length(gauge)
        for m = 1:grinding_freq_max
            table_interpol(g_id, m) = F(m, gauge(g_id));
        end
    end
end




