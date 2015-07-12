% Derive consensus graph
% over n_perms number iterations
% then write out the edgelist for the graph

path(path,'/home/andric/BCT2015');
cd('/cnari/normal_language/HEL/graph_analyses/group_modularity_thr0.5msk');
n_perms = 100;
diff_thr = 6
for td = [.05, .1, .15, .2]
    disp(td);
    disp(datestr(now))
    fname1 = sprintf('group_task_sess_%d.dens_%g.maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt', 1, td);
    M1 = dlmread(fname1);
    M1 = M1+1;
    m_ag1 = agreement(M1);
    fname2 = sprintf('group_task_sess_%d.dens_%g.maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt', 2, td);
    M2 = dlmread(fname2);
    M2 = M2+1;
    m_ag2 = agreement(M2);
    m_diff = m_ag1 - m_ag2;
    m_diff = abs(m_diff);
    m_diff(m_diff < diff_thr) = 0;

    [m, n] = size(m_diff);
    q_vec = zeros(n_perms, 1);
    mod_arr = zeros(m, n_perms);
    for ii = 1:n_perms
        [mod, q] = community_louvain(m_diff);
        q_vec(ii) = q;
        mod_arr(:,ii) = mod;
    end
    mod_fname = sprintf('group_task_diff_dens_%g.agreement.nothr.mod_arr', td)
    dlmwrite(mod_fname, mod_arr, ' ');

    q_fname = sprintf('group_task_diff_dens_%g.agreement.nothr.Qval', td)
    qfile = fopen(q_fname, 'w');
    for qn = 1:length(q_vec)
        fprintf(qfile, '%f\n', q_vec(qn));
    end
    fclose(qfile);
end
