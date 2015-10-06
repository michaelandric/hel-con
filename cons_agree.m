% get agreement about cluster

path(path,'/home/andric/BCT2015');
cd('/cnari/normal_language/HEL/graph_analyses/group_global_connectivity');

for cl = [2, 3]
    disp(cl)
    disp(datestr(now))
    fname = sprintf('group_Clust_msk_glob_conn_knnward_clst%d', cl);
    m = dlmread(fname);
    [nrows, ncols] = size(m);
    clst_mask = dlmread('Clust_mask.txt');
    clust = find(clst_mask == cl);

    new_m = m(clust, :);
    new_m = new_m + 1;
    ag_m = agreement(new_m);

    ag_m = ag_m / 18;
    ag_cons = consensus_und(ag_m, .3, 50);
    outvec = zeros(nrows, 1);
    outvec(clust, :) = ag_cons;

    out_fname = sprintf('consensus_prtn_knnward_clst%d_mskd', cl);
    out_f = fopen(out_fname, 'w');
    for m = 1:nrows
        fprintf(out_f, '%d\n', outvec(m));
    end
    fclose(out_f);
end
