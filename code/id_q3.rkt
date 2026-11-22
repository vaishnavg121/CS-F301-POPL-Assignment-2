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

;; Traverse preorder and postorder with suffix passing and no extra built-ins.
(define (preorder-onto tree suffix)
  (if (null? tree)
      suffix
      (cons (car tree)
            (preorder-onto (cadr tree)
                           (preorder-onto (caddr tree) suffix)))))

(define (postorder-onto tree suffix)
  (if (null? tree)
      suffix
      (postorder-onto (cadr tree)
                      (postorder-onto (caddr tree)
                                      (cons (car tree) suffix)))))

(define (print-all-traversals tree)
  (display (inorder-onto tree '()))
  (newline)
  (display (preorder-onto tree '()))
  (newline)
  (display (postorder-onto tree '()))
  (newline))

;; Return (height leaf-count) while visiting each subtree only once.
(define (tree-metrics tree)
  (if (null? tree)
      (list 0 0)
      (let* ((left (cadr tree))
             (right (caddr tree))
             (left-metrics (tree-metrics left))
             (right-metrics (tree-metrics right)))
        (list (+ 1 (max (car left-metrics) (car right-metrics)))
              (if (and (null? left) (null? right))
                  1
                  (+ (cadr left-metrics) (cadr right-metrics)))))))

(define (print-height-and-leaves tree)
  (display (tree-metrics tree))
  (newline))
