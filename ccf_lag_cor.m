% get pairwise rho
% and detect community structure

path(path,'/home/andric/BCT2015');
ccfdir = sprintf('/home/cnari/cnari_projects/normal_language/HEL/ccf_cor/');
cd(ccfdir);

subjs = linspace(1, 19, 19);
subjs(9) = []

n_vox = 20071;
subj_mat = zeros(length(subjs), n_vox);
for s = 1:length(subjs)
    fname = sprintf('ccf_abs_lag_out_hel%d_gm_mskd.ijk_fnirted_MNI4mm_thr0.5.txt', subjs(s));
    subj_mat(s, :) = dlmread(fname);
end

rho = corr(subj_mat, 'Type', 'Spearman');
rho(rho < 0) = 0;

% [mem, qual] = community_louvain(rho);
% below function accepts negative weights
% tic; [mm3 qq3] = modularity_louvain_und_sign(rho); toc;

n_perms = 100;
q_vec = zeros(n_perms, 1);
mod_arr = zeros(n_vox, n_perms);
for i = 1:n_perms
    disp('iter %d', i)
    disp(datestr(now))
    [mem, qual] = modularity_louvain_und_sign(rho);
    q_vec(i) = qual;
    mod_arr(:, i) = mem;
end

mod_fname = sprintf('ccf_abs_lag_out.no_thresh.mod_arr')
dlmwrite(mod_fname, mod_arr, ' ');

q_fname = sprintf('ccf_abs_lag_out.no_thresh.qval')
qfile = open(q_fname, 'w');
for qn = 1:length(q_vec)
    fprintf(qfile, '%f\n', q_vec(qn));
end
fclose(qfile);

