
fname1 = sprintf('group_task_sess_%d.dens_%g.maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt', 1, td);
M1 = dlmread(fname1);
M1 = M1+1;
ag1 = agreement(M1);

fname2 = sprintf('group_task_sess_%d.dens_%g.maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt', 2, td);
M2 = dlmread(fname2);
M2 = M2+1;
ag2 = agreement(M2);


% m_diff(m_diff <= diff_thr) = 0;
% m_diff(m_diff > 0) = 1;

new_thr = 14;
new_thr = 12;
new_thr = 15;
new_thr = 16;
new_thr = 17;
ag1(ag1 <= new_thr) = 0;
ag1(ag1 > 0) = 1;
[ag1_cmp, ag1_cmp_sz] = get_components(ag1);

ag2(ag2 <= new_thr) = 0;
ag2(ag2 > 0) = 1;
[ag2_cmp, ag2_cmp_sz] = get_components(ag2);

ag1_max_val = find(ag1_cmp_sz == max(ag1_cmp_sz));
ag2_max_val = find(ag2_cmp_sz == max(ag2_cmp_sz));

ag1_cmp(find(ag1_cmp ~= ag1_max_val)) = 0;
ag1_cmp(find(ag1_cmp == ag1_max_val)) = 1;
ag2_cmp(find(ag2_cmp ~= ag2_max_val)) = 0;
ag2_cmp(find(ag2_cmp == ag2_max_val)) = 1;

diff_cmp = ag1_cmp - ag2_cmp;
diff_cmp(find(diff_cmp == -1)) = 2;

cmp_outname = sprintf('diff_tasks_large_comp_dens_%g_thr%g.vals', new_thr, td)
cmp_file = fopen(cmp_outname, 'w')
for c = 1:length(diff_cmp)
    fprintf(cmp_file, '%d\n', diff_cmp(c));
end
fclose(cmp_file);

cmp_outname = sprintf('task1_large_comps_dens_%g_thr%g.vals', new_thr, td)
cmp_file = fopen(cmp_outname, 'w')
for c = 1:length(ag1_cmp)
    fprintf(cmp_file, '%d\n', ag1_cmp(c));
end
fclose(cmp_file);

cmp_outname = sprintf('task2_large_comps_dens_%g_thr%g.vals', new_thr, td)
cmp_file = fopen(cmp_outname, 'w')
for c = 1:length(ag2_cmp)
    fprintf(cmp_file, '%d\n', ag2_cmp(c));
end
fclose(cmp_file);
