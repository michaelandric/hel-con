% correlate group_task_sess* matrices
% finding similarity at vertices

path(path,'/home/andric/BCT2015');
cd('/cnari/normal_language/HEL/graph_analyses/group_modularity_thr0.5msk');

for sess = [1, 2]
    task_d05 = dlmread(sprintf('group_task_sess_%d.dens_0.05.maxq_tree', sess));
    ag_task_d05 = agreement(task_d05);
    task_d10 = dlmread(sprintf('group_task_sess_%d.dens_0.1.maxq_tree', sess));
    ag_task_d10 = agreement(task_d10);
    task_d15 = dlmread(sprintf('group_task_sess_%d.dens_0.15.maxq_tree', sess));
    ag_task_d15 = agreement(task_d15);
    task_d20 = dlmread(sprintf('group_task_sess_%d.dens_0.2.maxq_tree', sess));
    ag_task_d20 = agreement(task_d20);
    corr_vec = zeros(6, 1);
    corr_vec(1) = corr2(ag_task_d05, ag_task_d10);
    corr_vec(2) = corr2(ag_task_d05, ag_task_d15);
    corr_vec(3) = corr2(ag_task_d05, ag_task_d20);
    corr_vec(4) = corr2(ag_task_d10, ag_task_d15);
    corr_vec(5) = corr2(ag_task_d10, ag_task_d20);
    corr_vec(6) = corr2(ag_task_d15, ag_task_d20);
    disp(corr_vec);
    outname = sprintf('group_task_sess_%d.corr_comparisons', sess);
    out_f = fopen(outname, 'w');
    for i = 1:6
        fprintf(out_f, '%f\n', corr_vec(i));
    end
end
