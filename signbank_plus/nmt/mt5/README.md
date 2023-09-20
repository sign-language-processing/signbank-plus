## mT5

### Train Systems
```bash
sbatch train.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/original \
  /shares/volk.cl.uzh/amoryo/checkpoints/mt5/original
  
sbatch train.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/cleaned \
  /shares/volk.cl.uzh/amoryo/checkpoints/mt5/cleaned
  
sbatch train.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/expanded \
  /shares/volk.cl.uzh/amoryo/checkpoints/mt5/expanded
```

### Eval Systems

Wait for all systems to finish training
```bash
sbatch eval.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test \
  /shares/volk.cl.uzh/amoryo/checkpoints/mt5/original
  
sbatch eval.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test \
  /shares/volk.cl.uzh/amoryo/checkpoints/mt5/cleaned
  
sbatch eval.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test \
  /shares/volk.cl.uzh/amoryo/checkpoints/mt5/expanded
  
cat /shares/volk.cl.uzh/amoryo/checkpoints/mt5/original/sacrebleu.txt
cat /shares/volk.cl.uzh/amoryo/checkpoints/mt5/cleaned/sacrebleu.txt
cat /shares/volk.cl.uzh/amoryo/checkpoints/mt5/expanded/sacrebleu.txt
```

