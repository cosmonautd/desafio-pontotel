<script>
import { Line, mixins } from 'vue-chartjs'

const { reactiveProp } = mixins

export default {
	extends: Line,
	mixins: [reactiveProp],
	props: ['chartdata', 'options'],
	mounted () {
		this.renderChart(this.chartdata, this.options)
	}
}
</script>

<style scoped>
</style>