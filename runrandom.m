function runrandom(subject, cond, st, fin)
disp(st)
% class(st)
links_file = ['/mnt/tier2/urihas/Andric/steadystate/links_files5p/',subject,'.',cond,'.5p_r0.5_linksthresh_proportion.out.links'];
disp(links_file)
edgelist=dlmread(links_file);
disp(size(edgelist))
edgelist=edgelist(:,1:2);
adjmat=zeros(max(max(edgelist+1)),'uint8');
for i=1:length(edgelist)
    adjmat(1+edgelist(i,1),1+edgelist(i,2))=1;
end
adjmat=adjmat+adjmat';
i = st;
while(i < fin)
    tic; randmat=sym_generate_srand(adjmat);
    [Ci Q] = modularity_louvain_und(randmat); toc
    dlmwrite(['/mnt/tier2/urihas/Andric/steadystate/links_files5p/rando_trees/rand_',num2str(i),'_',subject,'_',cond,'.tree'], Ci');
    i = i + 1;
end


%
% STARTING HERE
path(path,'/home/andric/BCT2015');

ss = 'hel1';
session = 1;
dens = .05;

cd(sprintf('/cnari/normal_language/HEL/graph_analyses/%s/', ss));
edgelist_name = sprintf('graphs/task_sess_%d_%s.dens_%g.edgelist', session, ss, dens);
edgelist_name_gz = sprintf('%s.gz', edgelist_name);
gunzip(edgelist_name_gz);
el = dlmread(edgelist_name);
delete(edgelist_name);

el = el + 1;
[n_edges, ~] = size(el);
n_nodes = max(max(el));

w = repmat(1, n_edges, 1);
% THIS GIVES ONLY UPPER TRIANGLE
m = sparse(el(:, 1), el(:, 2), w, n_nodes, n_nodes);
mm = full(m);
% FILL OUT THE TRIUL GET COMPLETE ADJ MATRIX
A = mm + triu(mm, 1)';

