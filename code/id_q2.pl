% P2 implementation unit: expression/3.
% expression(+Numbers, -Tree, -IntegerValue) enumerates every ordered
% binary expression tree using exactly Numbers as its leaves.
% Tree uses num(N) for leaves and op(Operator, Left, Right) for nodes.
% This unit constructs and evaluates trees; formatting and equations are
% separate predicates developed in later units.

expression([N], num(N), N) :-
    integer(N),
    N >= 0.

expression(Numbers, Tree, Value) :-
    append(LeftNumbers, RightNumbers, Numbers),
    LeftNumbers = [_|_],
    RightNumbers = [_|_],
    expression(LeftNumbers, LeftTree, LeftValue),
    expression(RightNumbers, RightTree, RightValue),
    (   Tree = op('+', LeftTree, RightTree),
        Value is LeftValue + RightValue
    ;   Tree = op('-', LeftTree, RightTree),
        Value is LeftValue - RightValue
    ;   Tree = op('*', LeftTree, RightTree),
        Value is LeftValue * RightValue
    ;   RightValue =\= 0,
        0 is LeftValue mod RightValue,
        Tree = op('/', LeftTree, RightTree),
        Value is LeftValue // RightValue
    ).

% format_expression(+Tree, -String)
% Serialize an expression tree with the minimal parentheses required to
% preserve its structure under standard precedence and left associativity.
% Leaves are non-negative integers; result is an SWI-Prolog string.
format_expression(num(N), String) :-
    integer(N),
    N >= 0,
    number_string(N, String).

format_expression(op(Op, Left, Right), String) :-
    memberchk(Op, ['+', '-', '*', '/']),
    format_expression(Left, LeftBare),
    format_expression(Right, RightBare),
    (   memberchk(Op, ['*', '/'])
    ->  ParentPrecedence = 2
    ;   ParentPrecedence = 1
    ),
    % The left operand needs parentheses only for lower precedence.
    (   Left = op(LeftOp, _, _)
    ->  (   memberchk(LeftOp, ['*', '/'])
        ->  LeftPrecedence = 2
        ;   LeftPrecedence = 1
        ),
        (   LeftPrecedence < ParentPrecedence
        ->  format(string(LeftString), '(~s)', [LeftBare])
        ;   LeftString = LeftBare
        )
    ;   LeftString = LeftBare
    ),
    % Equal precedence on the right must also be parenthesized to retain
    % the tree, even for associative operators such as + and *.
    (   Right = op(RightOp, _, _)
    ->  (   memberchk(RightOp, ['*', '/'])
        ->  RightPrecedence = 2
        ;   RightPrecedence = 1
        ),
        (   RightPrecedence =< ParentPrecedence
        ->  format(string(RightString), '(~s)', [RightBare])
        ;   RightString = RightBare
        )
    ;   RightString = RightBare
    ),
    format(string(String), '~s~w~s', [LeftString, Op, RightString]).

% generate_equation(+List, -Equation)
% Split the given numbers at exactly one equals sign, retaining their order.
% Both expression trees are evaluated before their strings are constructed.
generate_equation(List, Equation) :-
    append(LeftNumbers, RightNumbers, List),
    LeftNumbers = [_|_],
    RightNumbers = [_|_],
    expression(LeftNumbers, LeftTree, Value),
    expression(RightNumbers, RightTree, Value),
    format_expression(LeftTree, LeftText),
    format_expression(RightTree, RightText),
    format(string(Equation), '~s=~s', [LeftText, RightText]).

% all_equations(+List, -Equations)
% sort/2 orders SWI strings and removes any duplicate serializations.
all_equations(List, Equations) :-
    findall(Equation, generate_equation(List, Equation), Unsorted),
    sort(Unsorted, Equations).

% count_equations(+List, -N)
% Count the distinct valid equation strings, not the search derivations.
count_equations(List, N) :-
    all_equations(List, Equations),
    length(Equations, N).
