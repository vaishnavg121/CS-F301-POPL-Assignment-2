#lang racket/base

;; S1: build inorder values using an accumulator suffix.
;; Passing the suffix directly avoids forbidden append and reverse helpers.
(define (inorder-onto tree suffix)
  (if (null? tree)
      suffix
      (inorder-onto (cadr tree)
                    (cons (car tree)
                          (inorder-onto (caddr tree) suffix)))))

(define (print-inorder tree)
  (display (inorder-onto tree '()))
  (newline))
