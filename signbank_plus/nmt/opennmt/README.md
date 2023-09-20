## opennmt

### Train Systems
```bash
sbatch train.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/original \
  /shares/volk.cl.uzh/amoryo/checkpoints/opennmt/original
  
sbatch train.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/cleaned \
  /shares/volk.cl.uzh/amoryo/checkpoints/opennmt/cleaned
   
sbatch train.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/expanded \
  /shares/volk.cl.uzh/amoryo/checkpoints/opennmt/expanded 

```

### Eval Systems

Wait for all systems to finish training
```bash
sbatch eval.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test \
  /shares/volk.cl.uzh/amoryo/checkpoints/opennmt/original
  
sbatch eval.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test \
  /shares/volk.cl.uzh/amoryo/checkpoints/opennmt/cleaned
  
sbatch eval.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test \
  /shares/volk.cl.uzh/amoryo/checkpoints/opennmt/expanded
```

