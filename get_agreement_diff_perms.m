% Derive agg graph
% over n_perms number iterations
% write out the difference component
% write out the max component size
% then permute and write out the permuted components

path(path,'/home/andric/BCT2015');
cd('/cnari/normal_language/HEL/graph_analyses/group_modularity_thr0.5msk');

diff_thr = 8
n_perms = 1000;
perm_a = dlmread('perm_mat_a.txt');
perm_b = dlmread('perm_mat_b.txt');
[perms_available, nsubj] = size(perm_a);

% for td = [.05, .1, .15, .2]
for td = [.05, .15]
    disp(td);
    disp(datestr(now))
    fname1 = sprintf('group_task_sess_%d.dens_%g.maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt', 1, td);
    M1 = dlmread(fname1);
    M1 = M1+1;
    fname2 = sprintf('group_task_sess_%d.dens_%g.maxq_tree.ijk_fnirted_MNI4mm_thr0.5.txt', 2, td);
    M2 = dlmread(fname2);
    M2 = M2+1;
    M = [M1, M2];

    m_ag1 = agreement(M1);
    m_ag2 = agreement(M2);
    m_diff = abs(m_ag1 - m_ag2);
    m_diff(m_diff <= diff_thr) = 0;
    m_diff(m_diff > 0) = 1;
    [cmp, cmp_sz] = get_components(m_diff);

    oo = find(cmp_sz(:) == 1);
    [~, vv] = ismember(oo, cmp);
    cmp(vv) = 0;

    cmp_outname = sprintf('group_task_diff_thr%d_component_dens_%g.vals', diff_thr, td)

    cmp_file = fopen(cmp_outname, 'w');
    for c = 1:length(cmp)
        fprintf(cmp_file, '%d\n', cmp(c));
    end
    fclose(cmp_file);

    cmp_size_name = sprintf('group_task_diff_thr%d_component_dens_%g.cmp_size', diff_thr, td)
    cmp_size_file = fopen(cmp_size_name, 'w');
    fprintf(cmp_size_file, '%d\n', max(cmp_sz));
    fclose(cmp_size_file);

    perm_vec = zeros(n_perms, 1);
    for i = 1:n_perms
        r = randperm(perms_available, 1);
        M_a = M(:,perm_a(r, :));
        M_b = M(:,perm_b(r, :));
        a_ag = agreement(M_a);
        b_ag = agreement(M_b);

        m_diff = abs(a_ag - b_ag);
        m_diff(m_diff <= diff_thr) = 0;
        m_diff(m_diff > 0) = 1;
        [cmp, cmp_sz] = get_components(m_diff);
        perm_vec(i) = max(cmp_sz);
    end

    sorted_perm_vec = sort(perm_vec);

    pv_outname = sprintf('group_task_diff_thr%d_component_dens_%g.perm_vec', diff_thr, td)
    pv_file = fopen(pv_outname, 'w');
    for pv = 1:length(sorted_perm_vec)
        fprintf(pv_file, '%d\n', sorted_perm_vec(pv));
    end
    fclose(pv_file);
end
