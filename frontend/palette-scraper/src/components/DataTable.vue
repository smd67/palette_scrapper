<!-- DataTable.vue -->
<template>
    <div class="my-division">
      <div class="my-division">
        <Input @button-clicked="fetchTableData" @data-sent="handleData" @download-data="downloadData"/>
      </div>
      <div class="spinner" v-if="isLoading"></div>
      <div>
        <table v-if="tableData.length > 0">
            <thead>
            <tr>
                <th>Name</th>
                <th>Color List</th>
                <!-- Add more table headers as needed -->
            </tr>
            </thead>
            <tbody>
            <tr v-for="item in filteredData" :key="item.palette_name">
                <td>{{ item.palette_name }}</td>
                <td>
                  <div class="grid-container" :key="item.palette_name">
                    <div v-for="my_color in item.color_list" :key="item.palette_name">
                      <div class="grid-item" :style="{ backgroundColor:  my_color }"> {{ my_color }} </div>
                    </div>
                  </div>
                </td>
                <!-- Display more data properties as needed -->
            </tr>
            </tbody>
        </table>
      </div>
    </div>
  </template>

  <script>
  import axios from 'axios';
  import Input from './Input.vue';

  export default {
    components: { Input },
    data() {
      return {
        tableData: [], // This array will store the fetched data
        url: '',
        isLoading: false,
        showDiv: false,
        filteredData: []
      };
    },
    methods: {
      handleData(data) {
        this.url = data;
      },
      async fetchTableData() {
        const apiUrl = 'http://127.0.0.1:8001/get-palettes/'; // Replace with your actual API endpoint
        const config = {
            headers: {
                'Content-Type': 'application/json'
            }
        };
        const requestBody = {
            url: this.url
        }
        try {
          this.isLoading = true;
          const response = await axios.post(apiUrl, requestBody, config);
          this.tableData = response.data; // Assign the fetched data to tableData
          this.filteredData = this.tableData.map(obj => {
            // This regex matches any character that is NOT a letter (a-z, A-Z) or a digit (0-9).
            // The 'g' flag ensures all occurrences are replaced, not just the first.
            obj.palette_name = obj.palette_name.replace(/[^a-zA-Z0-9]/g, '');
            obj.palette_name =obj.palette_name.charAt(0).toLowerCase() + obj.palette_name.slice(1);
            return obj;
          });
        } catch (error) {
          console.error('Error fetching data:', error);
        } finally {
          this.isLoading = false;
        }
      },
      downloadData() {
        var paletteData = {};
        this.filteredData.map(obj => {
          paletteData[obj.palette_name] = obj.color_list;
          return obj;
        });
        
        const dataString = "export const palettes = " + JSON.stringify(paletteData, null, 2); // Pretty print JSON
        const blob = new Blob([dataString], { type: 'application/json' });

        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'palettes.js';

        document.body.appendChild(link); // Append to body (optional, but ensures clickability in some environments)
        link.click();
        document.body.removeChild(link); // Clean up
        URL.revokeObjectURL(link.href);
      },
    },
  };
  </script>

  <style scoped>
  /* Add basic styling for the table if needed */
  table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  th {
    background-color: #f2f2f2;
  }
  .my-division {
    padding-top: 82px;
    padding-bottom: 30px;
  }
  .spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: #3498db;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
  }
  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
  .grid-container {
    display: grid;
    grid-template-columns: repeat(5, 1fr); /* 5 columns, equal width */
    grid-template-rows: repeat(1, auto); /* 1 rows, height determined by content */
    gap: 1px; /* Adjust as needed for spacing */
  }
  .grid-item {  
    /* Optional: Add styling for individual grid items */
    display: inline-block;
    border: 1px solid #ccc;
    padding: 1px;
  }
  </style>