% Derive consensus graph
% over n_perms number iterations
% then write out the edgelist for the graph

path(path,'/home/andric/BCT2015');
cd('/cnari/normal_language/HEL/graph_analyses/subrun_group_modularity_thr0.5msk');
n_perms = 100;

for td = [.15]
    for session = {'first', 'second'}
        disp(td);
        disp(datestr(now))
        fname1 = sprintf('group_task_sess_%s.dens_%g.maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt', session{1}, td)
        M = dlmread(fname1);
        M = M+1;
        disp(size(M))
        [m, n] = size(M);

        m_ag = agreement(M);
        q_vec = zeros(n_perms, 1);
        mod_arr = zeros(m, n_perms);
        for ii = 1:n_perms
            [mod, q] = community_louvain(m_ag);
            q_vec(ii) = q;
            mod_arr(:,ii) = mod;
        end
        mod_fname = sprintf('group_task_sess_%s.dens_%g.agreement.nothr.mod_arr', session{1}, td)
        dlmwrite(mod_fname, mod_arr, ' ');

        q_fname = sprintf('group_task_sess_%s.dens_%g.agreement.nothr.Qval', session{1}, td)
        qfile = fopen(q_fname, 'w');
        for qn = 1:length(q_vec)
            fprintf(qfile, '%f\n', q_vec(qn));
        end
        fclose(qfile);
    end
end
