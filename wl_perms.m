% testing WL kernels in matlab
% http://www.jmlr.org/papers/volume12/shervashidze11a/shervashidze11a.pdf
% http://mlcb.is.tuebingen.mpg.de/Mitarbeiter/Nino/Graphkernels/
path(path,'/home/andric/BCT2015');
path(path,'/home/andric/graphkernels');
path(path,'/home/andric/graphkernels/labeled');

cd('/cnari/normal_language/HEL/graph_analyses/group_modularity_thr0.5msk');

td = .15;
diff_thr = 8
n_perms = 1000;
perm_a = dlmread('perm_mat_a.txt');
perm_b = dlmread('perm_mat_b.txt');
[perms_available, nsubj] = size(perm_a);

fname1 = sprintf('group_task_sess_%d.dens_%g.maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt', 1, td);
M1 = dlmread(fname1);
M1 = M1+1;
fname2 = sprintf('group_task_sess_%d.dens_%g.maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt', 2, td);
M2 = dlmread(fname2);
M2 = M2+1;
M = [M1, M2];

perm_vec = zeros(n_perms, 1);
for i = 1:n_perms
    tic;
    r = randperm(perms_available, 1);
    M_a = M(:,perm_a(r, :));
    M_b = M(:,perm_b(r, :));
    a_ag = agreement(M_a);
    a_ag(a_ag < diff_thr) = 0;
    b_ag = agreement(M_b);
    b_ag(b_ag < diff_thr) = 0;
    ags = struct('am', {}, 'al', {});
    ags(1).am = a_ag;
    ags(2).am = b_ag;
    ags(1).al = cellfun(@(x) find(x),num2cell(a_ag,2),'un',0);
    ags(2).al = cellfun(@(x) find(x),num2cell(b_ag,2),'un',0);
    [km, rt] = WL(ags, 1, 0);
    nrm_km = normalizekm(km{1});
    perm_vec(i) = nrm_km(1, 2);
    toc;

end

sorted_perm_vec = sort(perm_vec);
pv_outname = sprintf('wl_similarity_diffthr%d_dens_%g.perm_vec', diff_thr, td)
pv_file = fopen(pv_outname, 'w');
for pv = 1:length(sorted_perm_vec)
    fprintf(pv_file, '%d\n', sorted_perm_vec(pv));
end
fclose(pv_file);


m_ag1 = agreement(M1);
m_ag2 = agreement(M2);
m_ag1(m_ag1 < diff_thr) = 0;
m_ag2(m_ag2 < diff_thr) = 0;
ags = struct('am', {}, 'al', {})
ags(1).am = m_ag1;
ags(2).am = m_ag2;
ags(1).al = cellfun(@(x) find(x),num2cell(m_ag1,2),'un',0)
ags(2).al = cellfun(@(x) find(x),num2cell(m_ag2,2),'un',0)

[km, rts] = WL(ags, 1, 0);
val_nrm_km = normalizekm(km{1});
km_simval_name = sprintf('wl_similarity_diffthr%d_dens_%g.wl_simval', diff_thr, td);
km_simval_file = fopen(km_simval_name, 'w');
fprintf(km_simval_file, '%d\n', val_nrm_km(1, 2));
fclose(km_simval_file);

