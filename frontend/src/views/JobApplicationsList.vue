<template>
  <div>
    <h1>Job Applications</h1>
    <table>
      <thead>
        <tr>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Address</th>
          <th>Expected Salary</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="app in applications" :key="app.id">
          <td>{{ app.first_name }}</td>
          <td>{{ app.last_name }}</td>
          <td>{{ app.address }}</td>
          <td>{{ app.expected_salary }}</td>
          <td>
            <button @click="editApplication(app)">Edit</button>
            <button @click="deleteApplication(app.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <button @click="exportData">Export to CSV</button>
    <h1>Upload CSV</h1>
    <form @submit.prevent="uploadCSV">
      <input type="file" @change="handleFileUpload" />
      <button type="submit">Upload</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      applications: [],
    };
  },
  async created() {
    this.loadApplications();
  },
  methods: {
    async loadApplications() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/applications/');
        this.applications = response.data;
      } catch (error) {
       
      }
      
    },
    async editApplication(application) {
      // Implement edit functionality
    },
    async deleteApplication(id) {
      try {
        await axios.delete(`http://127.0.0.1:8000/applications/${id}`);
        this.loadApplications();
      } catch (error) {
        console.error(error);
      }
    },
    async exportData() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/export/', {
          responseType: 'blob' // กำหนด responseType เป็น 'blob' เพื่อรองรับไฟล์ที่ดาวน์โหลด
        });

        // สร้างลิงก์ดาวน์โหลดไฟล์
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'applications.csv'); // กำหนดชื่อไฟล์ที่ต้องการดาวน์โหลด
        document.body.appendChild(link);
        link.click();
      } catch (error) {
        console.error('Error downloading the file:', error);
      }
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadCSV() {
      const formData = new FormData();
      formData.append("file", this.selectedFile);

      try {
        await this.$axios.post("http://127.0.0.1:8000/upload-csv/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        alert("File uploaded successfully");
      } catch (error) {
        alert("Failed to upload file");
      }
    },
  },
};
</script>
