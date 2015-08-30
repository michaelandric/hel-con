% get agreement about cluster

path(path,'/home/andric/BCT2015');
cd('/cnari/normal_language/HEL/graph_analyses/group_global_connectivity');

fname = sprintf('group_Clust_msk_glob_conn_knnward_clst1');
m = dlmread(fname);
[nrows, ncols] = size(m);
m_rsum = sum(m, 2);
keeprows = find(m_rsum > 0);

new_m = m(keeprows, :);
new_m = new_m + 1;
ag_m = agreement(new_m);

[com, q] = community_louvain(ag_m);
[com, q] = community_louvain(ag_m_thr);
w_cl = clusterdata(ag_m, 'ward');
w_cl = clusterdata(ag_m,'linkage','ward','savememory','on','maxclust',4);

m_rsum(keeprows, :) = w_cl;
m_rsum(keeprows, :) = w_cl_thr;
m_rsum(keeprows, :) = com';
out_fname = sprintf('group_Clust_msk_glob_conn_knnward_clst1_array')
out_fname = sprintf('group_Clust_msk_glob_conn_knnward_clst1_arraythr')
out_fname = sprintf('group_Clust_msk_glob_conn_knnward_clst1_arraythr14')
out_fname = sprintf('group_Clust_msk_glob_conn_knnward_clst1_arraycom')
dlmwrite(out_fname, m_rsum, ' ');


% testing these things:
ag_m_thr = ag_m;
ag_m_thr(ag_m_thr < 11) = 0;
ag_m_thr(ag_m_thr > 0) = 1;
w_cl_thr = clusterdata(ag_m_thr,'linkage','ward','savememory','on','maxclust',4);

ag_m_thr = ag_m;
ag_m_thr(ag_m_thr < 14) = 0;
ag_m_thr(ag_m_thr > 0) = 1;
w_cl_thr = clusterdata(ag_m_thr,'linkage','ward','savememory','on','maxclust',4);
m_rsum(keeprows, :) = w_cl_thr;
out_fname = sprintf('group_Clust_msk_glob_conn_knnward_clst1_arraythr14')
dlmwrite(out_fname, m_rsum, ' ');


dlmwrite('agreement_group_Clust_msk_glob_conn_knnward_clst1', ag_m, ' ');


pv_outname = sprintf('ag_keeprows2')
pv_file = fopen(pv_outname, 'w');
for pv = 1:length(keeprows)
    fprintf(pv_file, '%d\n', keeprows(pv));
end
fclose(pv_file);
