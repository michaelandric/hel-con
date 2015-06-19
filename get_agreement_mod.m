% Derive consensus graph
% first permute agreement to see what you
% get by chance
% then write out the edgelist for the graph

path(path,'/home/andric/BCT2015');
cd('/cnari/normal_language/HEL/graph_analyses/group_modularity');
M = dlmread('group_task_sess_1.dens_0.05.maxq_tree.ijk_fnirted_MNI4mm.txt');
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

% ff = find(m_ag > 14);
% m_ag(ff) = 0;

m_ag = agreement(M);
[mod, q] = community_louvain(m_ag);
modfile = fopen('group_task_sess_1.dens_0.05.agreement.nothr.mods', 'w');
for m in 1:length(mod)
    fprintf(modfile, '%d\n', mods(m));
end
fclose(modfile);
qfile = fopen('group_task_sess_1.dens_0.05.agreement.nothr.Qval', 'w');
fprintf(qfile, '%d\n', q);
fclose(qfile);


[r, c] = find(m_ag > max(perm_vec));
fileID = fopen('group_task_sess_1.dens_0.05.agreement.thr.edgelist', 'w');
for k = 1:length(r)
    fprintf(fileID, '%d %d\n', r(k), c(k));
end
fclose(fileID);

% binary format
%fileID = fopen('group_task_sess_1.dens_0.05.agreement.edgelist.bin', 'w');
%fwrite(fileID, [r, c], 'integer*4');
%fclose(fileID);

% [mod, q] = community_louvain(m_ag);
