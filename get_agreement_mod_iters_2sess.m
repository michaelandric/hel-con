% Derive consensus graph
% over n_perms number iterations
% then write out the edgelist for the graph

path(path,'/home/andric/BCT2015');
cd('/cnari/normal_language/HEL/graph_analyses/group_modularity_thr0.5msk');
for td = [.05, .1, .15, .2]
    disp(td);
    disp(datestr(now))
    fname1 = sprintf('group_task_sess_%d.dens_%g.maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt', 1, td)
    M1 = dlmread(fname1);
    fname2 = sprintf('group_task_sess_%d.dens_%g.maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt', 2, td)
    M2 = dlmread(fname2);
    M = [M1, M2];
    M = M+1;
    disp(size(M))
    [m, n] = size(M);

    n_perms = 100

    m_ag = agreement(M);
    q_vec = zeros(n_perms, 1);
    mod_arr = zeros(m, n_perms);
    for ii = 1:n_perms
        [mod, q] = community_louvain(m_ag);
        q_vec(ii) = q;
        mod_arr(:,ii) = mod;
    end
    mod_fname = sprintf('group_task_2sess_dens_%g.agreement.nothr.mod_arr', td)
    dlmwrite(mod_fname, mod_arr, ' ');

    q_fname = sprintf('group_task_2sess_dens_%g.agreement.nothr.Qval', td)
    qfile = fopen(q_fname, 'w');
    for qn = 1:length(q_vec)
        fprintf(qfile, '%f\n', q_vec(qn));
    end
    fclose(qfile);
end
