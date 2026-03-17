<template>
  <div class="stats-dashboard">
    <h2>阅读统计</h2>
    <div ref="chartRef" class="chart-container"></div>

    <div class="stats">
      <p>阅读书籍总数：{{ totalBooks }}</p>
      <p>笔记总数：{{ totalJournals }}</p>
      <p>平均每本书的笔记数：{{ avgJournalsPerBook }}</p>
    </div>
  </div>
</template>

<script>
import { useBookStore } from '../stores/books.js';
import { useJournalStore } from '../stores/journals.js';
import { ref, computed, onMounted, watch } from 'vue';
import * as echarts from 'echarts';

export default {
  name: 'StatisticsDashboard',
  setup() {
    const bookStore = useBookStore();
    const journalStore = useJournalStore();

    const chartRef = ref(null);
    let chartInstance = null;

    const totalBooks = computed(() => bookStore.books.length);
    const totalJournals = computed(() => journalStore.journals.length);
    const avgJournalsPerBook = computed(() => {
      return totalBooks.value
        ? (totalJournals.value / totalBooks.value).toFixed(2)
        : 0;
    });

    const genreDistribution = computed(() => {
      const map = {};
      bookStore.books.forEach((book) => {
        const genre = book.genre || '未分类';
        map[genre] = (map[genre] || 0) + 1;
      });
      return Object.entries(map)
        .sort((a, b) => b[1] - a[1])
        .map(([genre, count]) => ({ genre, count }));
    });

    const renderChart = () => {
      if (!chartRef.value) return;
      if (!chartInstance) {
        chartInstance = echarts.init(chartRef.value);
      }

      const option = {
        title: {
          text: '按文学题材的阅读书籍分布',
          left: 'center',
          textStyle: {
            color: '#5d4e37',
            fontFamily: 'Georgia, serif',
          },
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
        },
        xAxis: {
          type: 'category',
          data: genreDistribution.value.map((d) => d.genre),
          axisLabel: {
            rotate: 40,
            interval: 0,
            color: '#5d4e37',
          },
        },
        yAxis: {
          type: 'value',
          name: '书籍数',
          axisLabel: {
            color: '#5d4e37',
          },
        },
        series: [
          {
            name: '书籍数',
            type: 'bar',
            data: genreDistribution.value.map((d) => d.count),
            itemStyle: {
              color: 'rgba(212, 175, 55, 0.8)',
            },
          },
        ],
        grid: {
          left: '10%',
          right: '10%',
          bottom: '20%',
          containLabel: true,
        },
      };

      chartInstance.setOption(option);
    };

    onMounted(() => {
      renderChart();
      window.addEventListener('resize', () => {
        chartInstance && chartInstance.resize();
      });
    });

    watch(genreDistribution, () => {
      renderChart();
    });

    return {
      chartRef,
      totalBooks,
      totalJournals,
      avgJournalsPerBook,
    };
  },
};
</script>

<style scoped>
.stats-dashboard {
  max-width: 1000px;
  margin: 0 auto;
  padding: 30px;
  background: linear-gradient(135deg, #f4e4bc 0%, #f9f6f0 50%, #e8dcc0 100%);
  min-height: 100vh;
  font-family: 'Georgia', serif;
}

.stats-dashboard h2 {
  text-align: center;
  color: #5d4e37;
  font-family: 'Georgia', serif;
  font-size: 32px;
  margin-bottom: 40px;
  border-bottom: 3px solid #d4af37;
  padding-bottom: 15px;
  display: inline-block;
  width: 100%;
}

.chart-container {
  height: 450px;
  margin: 30px 0;
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 12px;
  box-shadow:
    0 4px 20px rgba(139, 115, 85, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid #e8dcc0;
  padding: 25px;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 25px;
  margin-top: 40px;
}

.stats p {
  background: linear-gradient(135deg, #fefcf8 0%, #f9f6f0 100%);
  border-radius: 12px;
  box-shadow:
    0 4px 20px rgba(139, 115, 85, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid #e8dcc0;
  padding: 25px;
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  color: #5d4e37;
  margin: 0;
  transition: all 0.3s ease;
}

.stats p:hover {
  transform: translateY(-3px);
  box-shadow:
    0 6px 25px rgba(139, 115, 85, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

/* Responsive Design */
@media (max-width: 768px) {
  .stats-dashboard {
    padding: 20px;
  }

  .stats-dashboard h2 {
    font-size: 28px;
  }

  .chart-container {
    height: 350px;
    padding: 20px;
  }

  .stats {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .stats p {
    font-size: 18px;
    padding: 20px;
  }
}
</style>
