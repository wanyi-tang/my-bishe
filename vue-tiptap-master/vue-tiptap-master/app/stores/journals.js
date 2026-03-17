import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useJournalStore = defineStore('journals', () => {
  const journals = ref(JSON.parse(localStorage.getItem('journals') || '[]'));

  const saveToStorage = () => {
    localStorage.setItem('journals', JSON.stringify(journals.value));
  };

  const addJournal = (journal) => {
    journal.id = Date.now();
    journal.date = new Date().toISOString();
    journals.value.push(journal);
    saveToStorage();
  };

  const updateJournal = (id, updatedJournal) => {
    const index = journals.value.findIndex(j => j.id === id);
    if (index !== -1) {
      journals.value[index] = { ...journals.value[index], ...updatedJournal };
      saveToStorage();
    }
  };

  const deleteJournal = (id) => {
    journals.value = journals.value.filter(j => j.id !== id);
    saveToStorage();
  };

  const getJournalsByBook = (bookId) => {
    return journals.value.filter(j => j.bookId === bookId);
  };

  return {
    journals,
    addJournal,
    updateJournal,
    deleteJournal,
    getJournalsByBook,
  };
});