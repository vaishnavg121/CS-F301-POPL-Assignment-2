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
