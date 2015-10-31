% get degrees of difference network 
% 
path(path,'/home/andric/BCT2015');
cd('/cnari/normal_language/HEL/graph_analyses/group_modularity_thr0.5msk');

diff_thr = 8

td = .15
fname1 = sprintf('group_task_sess_%d.dens_%g.maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt', 1, td);
M1 = dlmread(fname1);
M1 = M1+1;
fname2 = sprintf('group_task_sess_%d.dens_%g.maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt', 2, td);
M2 = dlmread(fname2);
M2 = M2+1;
M = [M1, M2];

m_ag1 = agreement(M1);
m_ag2 = agreement(M2);
m_diff = abs(m_ag1 - m_ag2);
m_diff(m_diff <= diff_thr) = 0;
m_diff(m_diff > 0) = 1;
% [cmp, cmp_sz] = get_components(m_diff);

m_diff_deg = degrees_und(m_diff);

outname = sprintf('degrees_group_task_diff_thr%d_component_dens_%g.vals', diff_thr, td)
out_file = fopen(outname, 'w');
for c = 1:length(m_diff_deg)
    fprintf(out_file, '%d\n', m_diff_deg(c));
end
fclose(out_file);

