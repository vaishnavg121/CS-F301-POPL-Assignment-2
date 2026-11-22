#lang racket/base

;; Compute a list's original top-level length in constant stack space.
(define (my-length lst)
  (let loop ((remaining lst) (count 0))
    (if (null? remaining)
        count
        (loop (cdr remaining) (+ count 1)))))

;; Tail-recursive reversal supports a linear-time custom map.
(define (my-reverse lst)
  (let loop ((remaining lst) (result '()))
    (if (null? remaining)
        result
        (loop (cdr remaining) (cons (car remaining) result)))))

(define (my-map fn lst)
  (let loop ((remaining lst) (result '()))
    (if (null? remaining)
        (my-reverse result)
        (loop (cdr remaining)
              (cons (fn (car remaining)) result)))))

;; Produce a list transformer for a supplied original-length predicate.
;; () is a nested list too, so test null? as well as pair? for child lists.
(define (make-inserter x len-ok?)
  (letrec ((walk
            (lambda (lst)
              (let ((new-elements
                     (my-map (lambda (element)
                               (if (or (pair? element) (null? element))
                                   (walk element)
                                   element))
                             lst)))
                (if (len-ok? (my-length lst))
                    (cons x new-elements)
                    new-elements)))))
    walk))
