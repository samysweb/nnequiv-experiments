# Benchmarks
This table gives an overview over the benchmarks used in the evaluation.
All benchmarks can be found in the folder `/benchmarks-versions`.

Name | Layers Network 1 | Layers Network 2 | Training | Relevant/Verified Property |
------|--------------------|--------------------|------------|--------------------------------| 
ACAS\_1\_1-trunc | 5-50-50-50-50-50-50-5 | 5-50-50-50-50-50-50-5 | Network taken from [1]: Weights truncated from 32-bit to 16-bit floats. Only used for comparative performance of ReluDiff. | $\epsilon$-equivalent on ACAS Xu property 1 [2] for $\epsilon=0.05$
ACAS\_1\_2-trunc | 5-50-50-50-50-50-50-5 | 5-50-50-50-50-50-50-5 | Network taken from [1]: Weights truncated from 32-bit to 16-bit floats. Only used for comparative performance of ReluDiff. | $\epsilon$-equivalent on ACAS Xu property 1 [2] for $\epsilon=0.05$
ACAS\_1\_1-retrain | 5-50-50-50-50-50-50-5 | 5-50-50-50-50-50-50-5 | Retrained on ACAS\_1\_1 [3] on uniformly at random chosen points of property 1 using student teacher [4] training with mean squared error loss | $\epsilon$-equivalent on ACAS Xu property 1 [2] for $\epsilon=0.05$ (verified up to $\epsilon=0.005$)
ACAS\_1\_2-retrain | 5-50-50-50-50-50-50-5 | 5-50-50-50-50-50-50-5 | Retrained on ACAS\_1\_1 [3] on uniformly at random chosen points of property 1 using student teacher [4] training with mean squared error loss | $\epsilon$-equivalent on ACAS Xu property 1 [2] for $\epsilon=0.05$ (verified up to $\epsilon=0.005$)
ACAS\_1\_1-student | 5-50-50-50-50-50-50-5 | 5-100-100-5 | Retrained on ACAS\_1\_1 [3] on uniformly at random chosen points of property 1 using student teacher [4] training with mean squared error loss | $\epsilon$-equivalent on ACAS Xu property 1 [2] for $\epsilon=0.05$ (verified up to $\epsilon=0.005$)
ACAS\_1\_2-student | 5-50-50-50-50-50-50-5 | 5-100-100-5 | Retrained on ACAS\_1\_1 [3] on uniformly at random chosen points of property 1 using student teacher [4] training with mean squared error loss | $\epsilon$-equivalent on ACAS Xu property 1 [2] for $\epsilon=0.05$
MNIST\_large-epsilon | 64-100-80-60-40-20-10 | 64-40-40-10 | First NN trained on scaled down MNIST [5]; Second NN trained using student-teacher training [4] using mean square error loss | $\epsilon$-equivalent on MNIST cluster center (a) in [6] with radius $\pm0.2$
MNIST\_small-top | 64-32-16-10 | 64-36-10 | NN previously used in [6]; Trained using student teacher training [4] | top-1 equivalent on MNIST cluster center (a) in [6] with radius $\pm0.7$
MNIST\_medium-top | 64-32-16-10 | 64-12-12-12-10 | NN previously used in [6]; Trained using student teacher training [4] | top-1 equivalent on MNIST cluster center (a) in [6] with radius $\pm0.7$
MNIST\_large-epsilon | 64-100-80-60-40-20-10 | 64-40-40-10 | First NN trained on scaled down MNIST [5]; Second NN trained using student-teacher training [4] using KL divergence loss | top1-equivalent on MNIST cluster center (c) in [6] with radius $\pm0.3$
MNIST\_larger-epsilon | 64-100-200-300-200-100-10 | 64-40-40-10 | First NN trained on scaled down MNIST [5]; Second NN trained using student-teacher training [4] using KL divergence loss | top1-equivalent on MNIST cluster center (c) in [6] with radius $\pm0.2$

## Bibliography
[1] B. Paulsen, J. Wang, and C. Wang, “Reludiff: differential verification of deep neural networks,” pp. 714–726, 2020.  
[2] G. Katz, C. Barrett, D. L. Dill, K. Julian, and M. J. Kochenderfer, “Reluplex: An efficient SMT solver for verifying deep neural networks,” in International Conference on Computer Aided Verification. Springer,2017, pp. 97–117.  
[3] K. D. Julian, J. Lopez, J. S. Brush, M. P. Owen, and M. J. Kochenderfer,“Policy compression for aircraft collision avoidance systems,” in2016IEEE/AIAA 35th Digital Avionics Systems Conference (DASC). IEEE,2016, pp. 1–10.  
[4] G. Hinton, O. Vinyals, and J. Dean, “Distilling the knowledge in a neural network,”arXiv preprint arXiv:1503.02531, 2015.  
[5] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-based learning applied to document recognition,” Proceedings of the IEEE, vol. 86,no. 11, pp. 2278–2324, 1998.  
[6] M. Kleine B ̈uning, P. Kern, and C. Sinz, “Verifying Equivalence Properties of Neural Networks with ReLU Activation Functions,” in Principles and Practice of Constraint Programming - 26th International Conference, CP 2020, Louvain-la-Neuve, Belgium, Proceedings, 2020.