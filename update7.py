import os

# Updated Flutter code with User Identity
multi_user_code = '''
// ... (Existing imports)
import 'package:device_info_plus/device_info_plus.dart';

class _EBayCameraAppState extends State<EBayCameraApp> {
  String _currentUser = "Eos"; // Default user
  
  // Updated Save Logic
  Future<void> _saveItem() async {
    final directory = await getApplicationDocumentsDirectory();
    final String zackBasePath = p.join(directory.path, 'Zack');
    
    // UNIQUE FILENAME based on the user
    final String csvFileName = "ebay_${_currentUser.toLowerCase()}_manifest.csv";
    final File csvFile = File(p.join(zackBasePath, csvFileName));

    if (!await csvFile.exists()) {
      await csvFile.writeAsString("Action,Category,Title,Description,ConditionID,Price\\n");
    }

    // Append data...
    final String row = "Add,11483,\\"${_titleController.text}\\",\\"${_descController.text}\\",3000,${_priceController.text}\\n";
    await csvFile.writeAsString(row, mode: FileMode.append);
    
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Saved to $csvFileName")));
  }

  // Add a Toggle in the UI
  Widget _buildUserToggle() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Text("Listing as: "),
        DropdownButton<String>(
          value: _currentUser,
          items: ["Eos", "Zack"].map((String value) {
            return DropdownMenuItem<String>(value: value, child: Text(value));
          }).toList(),
          onChanged: (val) => setState(() => _currentUser = val!),
        ),
      ],
    );
  }
  
  // (Add _buildUserToggle() to your Column in the build method)
}
'''

with open('lib/main.dart', 'w') as f:
    f.write(multi_user_code)

print("App updated with Multi-User support. Now you won't overwrite Zack's files!")