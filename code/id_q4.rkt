#lang racket/base

;; Compute a list's original top-level length in constant stack space.
(define (my-length lst)
  (let loop ((remaining lst) (count 0))
    (if (null? remaining)
        count
        (loop (cdr remaining) (+ count 1)))))
