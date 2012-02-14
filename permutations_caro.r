# Find probability of finding R2 values based on distribution created with permutations
# 2010-11-25
# Eric Normandeau

NB_PERM = 10000
OUTPUT_FILE = "results_caro_sans_ligne6_10000.txt"
data = read.table("data_caro_sans_ligne6.txt", header=T)

init.names = names(data)
comb.names

nb_col = ncol(data)
nb_comb = nb_col * (nb_col -1) / 2

corr = matrix(-99, 2, nb_comb)
perm = matrix(-99, NB_PERM, nb_comb)

temp_col = 0
for(i in seq(nb_col)) {
    for(j in seq(nb_col)) {
        if(j > i) {
            temp_col = temp_col + 1
            corr[1, temp_col] = summary(lm(data[,i] ~ data[,j]))$r.squared
            for(k in seq(NB_PERM)) {
                col1 = sample(data[,i], length(data[,i]))
                col2 = sample(data[,j], length(data[,j]))
                perm[k, temp_col] = summary(lm(col1 ~ col2))$r.squared
            }
            perm[, temp_col] = sort(perm[, temp_col])
            corr[2, temp_col] = length(perm[perm[, temp_col] > corr[1, temp_col], temp_col]) / NB_PERM
        }
    }
}

results = data.frame(rbind(corr, perm))
#names(results) = c("AB", "AC", "AD", "BC", "BD", "CD")

write.table(results, OUTPUT_FILE, quote=F, row.names=F, sep="\t")

print("All is said and done...")
print("The battle is lost and won.")
