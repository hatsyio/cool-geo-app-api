select p_gender, p_age, sum(amount)
from paystats
group by p_gender, p_age
;
