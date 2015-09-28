% get agreement about cluster

path(path,'/home/andric/BCT2015');
cd('/cnari/normal_language/HEL/graph_analyses/group_global_connectivity');

fname = sprintf('group_Clust_msk_glob_conn_knnward_clst1');
m = dlmread(fname);
[nrows, ncols] = size(m);
% m_rsum = sum(m, 2);
% keeprows = find(m_rsum > 0);
clst_mask = dlmread('Clust_mask.txt');
clust1 = find(clst_mask == 1);

% new_m = m(keeprows, :);
new_m = m(clust1, :);
new_m = new_m + 1;
ag_m = agreement(new_m);

ag_m = ag_m / 18;
% ag_cons = consensus_und(ag_m, .5, 100);
ag_cons = consensus_und(ag_m, .3, 50);
% m_rsum(keeprows, :) = ag_cons;
outvec = zeros(nrows, 1);
% m_rsum(clust1, :) = ag_cons;
outvec(clust1, :) = ag_cons;

out_fname = sprintf('consensus_prtn_knnward_clst1_mskd');
out_f = fopen(out_fname, 'w');
for m = 1:nrows
    fprintf(out_f, '%d\n', outvec(m));
end
fclose(out_f);

