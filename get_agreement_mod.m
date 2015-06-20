% Derive consensus graph
% first permute agreement to see what you
% get by chance
% then write out the edgelist for the graph

path(path,'/home/andric/BCT2015');
cd('/cnari/normal_language/HEL/graph_analyses/group_modularity');
for session = 1:2
    td = .1

    fname = sprintf('group_task_sess_%d.dens_%g.maxq_tree.ijk_fnirted_MNI4mm.txt', session, td)
    M = dlmread(fname);
    M = M+1;

    [m, n] = size(M);

    n_perms = 100
    perm_vec = zeros(n_perms, 1);
    for ii = 1:n_perms
        rand_mat = zeros(m, n);
        for i = 1:n
            idx = randperm(m);
            rand_mat(:, i) = M(idx, i);
        end
        ag_r = agreement(rand_mat);
        perm_vec(ii) = max(ag_r(:));
    end

    pv_fname = sprintf('group_task_sess_%d.dens_%g.agreement.perm_vec', session, td)
    perm_vec_file = fopen(pv_fname, 'W')
    for p = 1:n_perms
        fprintf(perm_vec_file, '%d\n', perm_vec(p));
    end
    fclose(perm_vec_file);

    m_ag = agreement(M);
    [mod, q] = community_louvain(m_ag);
    mod_fname = sprintf('group_task_sess_%d.dens_%g.agreement.nothr.mods', session, td)
    modfile = fopen(mod_fname, 'w');
    for m = 1:length(mod)
        fprintf(modfile, '%d\n', mod(m));
    end
    fclose(modfile);
    q_fname = sprintf('group_task_sess_%d.dens_%g.agreement.nothr.Qval', session, td)
    qfile = fopen(q_fname, 'w');
    fprintf(qfile, '%f\n', q);
    fclose(qfile);


    % 14 is the value at 95/100 for session 1
    srt_pv = sort(perm_vec);
    thr = srt_pv(95);
    [r, c] = find(m_ag > thr);
    length(r)
    el_fname = sprintf('group_task_sess_%d.dens_%g.agreement.thr.edgelist', session, td)
    fileID = fopen(el_fname, 'w');
    for k = 1:length(r)
        fprintf(fileID, '%d %d\n', r(k), c(k));
    end
    fclose(fileID);
end



% This below is scrap
% ---------------------------
% binary format
%fileID = fopen('group_task_sess_1.dens_0.05.agreement.edgelist.bin', 'w');
%fwrite(fileID, [r, c], 'integer*4');
%fclose(fileID);
