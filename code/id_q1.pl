% P1 implementation unit: clue/2.
% Each clause checks its numbered clue on a fully instantiated Solution.
% Other predicates are developed separately to preserve the assignment's
% one-predicate-per-AI-request process.

clue(1, Solution) :-
    member(p(Name, Dept, _, 'AI'), Solution),
    Dept \= research,
    Name \= 'Dana'.

clue(2, Solution) :-
    member(p('Alex', Dept, Lang, _), Solution),
    Dept \= development,
    Lang \= 'c++'.

clue(3, Solution) :-
    member(p(_, testing, python, _), Solution).

clue(4, Solution) :-
    member(p('Ben', Dept, _, web), Solution),
    Dept \= testing.

clue(5, Solution) :-
    member(p(_, design, java, _), Solution).

clue(6, Solution) :-
    member(p('Carla', Dept, _, Project), Solution),
    Project \= embedded,
    Dept \= development.

clue(7, Solution) :-
    member(p('Dana', Dept, Lang, _), Solution),
    Lang \= java,
    (Dept = research ; Dept = testing).

clue(8, Solution) :-
    member(p(_, research, Lang, data), Solution),
    Lang \= javascript.

% CLUE 9: The friend who prefers the AI project works in the testing department.
clue(9, Solution) :-
    member(p(_, testing, _, 'AI'), Solution).

% Generate all bijective assignments and keep exactly those satisfying Active.
% This generator deliberately checks clues only after all fields are ground.
solution_for_clues(Active, Solution) :-
    permutation([research, development, design, testing],
                [D_Alex, D_Ben, D_Carla, D_Dana]),
    permutation([python, java, 'c++', javascript],
                [L_Alex, L_Ben, L_Carla, L_Dana]),
    permutation(['AI', web, embedded, data],
                [P_Alex, P_Ben, P_Carla, P_Dana]),
    Solution = [p('Alex', D_Alex, L_Alex, P_Alex),
                p('Ben', D_Ben, L_Ben, P_Ben),
                p('Carla', D_Carla, L_Carla, P_Carla),
                p('Dana', D_Dana, L_Dana, P_Dana)],
    forall(member(N, Active), clue(N, Solution)).

% Count complete assignments satisfying precisely the selected clue numbers.
count_solutions(Active, N) :-
    findall(Solution, solution_for_clues(Active, Solution), Solutions),
    length(Solutions, N).

% Print one solution of the repaired puzzle in the required order and layout.
main :-
    once(solution_for_clues([1,2,3,4,5,6,7,8,9],
        [p('Alex', AlexDept, AlexLang, AlexProject),
         p('Ben', BenDept, BenLang, BenProject),
         p('Carla', CarlaDept, CarlaLang, CarlaProject),
         p('Dana', DanaDept, DanaLang, DanaProject)])),
    format('Alex = [~w, ~w, ~w]~n', [AlexDept, AlexLang, AlexProject]),
    format('Ben = [~w, ~w, ~w]~n', [BenDept, BenLang, BenProject]),
    format('Carla = [~w, ~w, ~w]~n', [CarlaDept, CarlaLang, CarlaProject]),
    format('Dana = [~w, ~w, ~w]~n', [DanaDept, DanaLang, DanaProject]).
