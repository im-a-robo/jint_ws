// supabaseClient.js
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://txqxjekgsyjgbbqlsefv.supabase.co/'; // Your Supabase URL
//const supabaseAnonKey = process.env.REACT_APP_SUPABASE_KEY; // Your Supabase Key
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR4cXhqZWtnc3lqZ2JicWxzZWZ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjg3NDYyMzYsImV4cCI6MjA0NDMyMjIzNn0.ontxdMCLNSZZf896omiHX1WRuvRPo6drj_7EqJSFodA'

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
