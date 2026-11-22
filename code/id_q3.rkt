#lang racket/base

;; Accumulate in reverse so each left subtree is visited before the right.
(define (inorder-reversed tree values)
  (if (null? tree)
      values
      (let ((after-left (inorder-reversed (cadr tree) values)))
        (inorder-reversed (caddr tree) (cons (car tree) after-left)))))

(define (preorder-reversed tree values)
  (if (null? tree)
      values
      (let ((after-left (preorder-reversed (cadr tree) (cons (car tree) values))))
        (preorder-reversed (caddr tree) after-left))))

(define (postorder-reversed tree values)
  (if (null? tree)
      values
      (let* ((after-left (postorder-reversed (cadr tree) values))
             (after-right (postorder-reversed (caddr tree) after-left)))
        (cons (car tree) after-right))))

(define (reverse-values values)
  (let loop ((remaining values) (result '()))
    (if (null? remaining)
        result
        (loop (cdr remaining) (cons (car remaining) result)))))

(define (print-inorder tree)
  (display (reverse-values (inorder-reversed tree '())))
  (newline))

(define (print-all-traversals tree)
  (print-inorder tree)
  (display (reverse-values (preorder-reversed tree '())))
  (newline)
  (display (reverse-values (postorder-reversed tree '())))
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
