<template>
  <div>
    <h1>Job Application Form</h1>
    <form @submit.prevent="submitForm">
      <label for="first_name">First Name:</label>
      <input v-model="form.first_name" id="first_name" required />

      <label for="last_name">Last Name:</label>
      <input v-model="form.last_name" id="last_name" required />

      <label for="address">Address:</label>
      <input v-model="form.address" id="address" required />

      <label for="expected_salary">Expected Salary:</label>
      <input v-model="form.expected_salary" type="number" id="expected_salary" required />

      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        first_name: '',
        last_name: '',
        address: '',
        expected_salary: '',
      },
    };
  },
  methods: {
    async submitForm() {
      try {
        await axios.post('http://127.0.0.1:8000/applications/', this.form);
        alert('Application submitted successfully!');
        this.form = { first_name: '', last_name: '', address: '', expected_salary: '' };
      } catch (error) {
        console.error(error);
        alert('Error submitting application.');
      }
    },
  },
};
</script>
